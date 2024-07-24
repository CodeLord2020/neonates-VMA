from pyke import knowledge_engine, krb_traceback
import sys


class NeonatalExpertSystem:
    def __init__(self):
        self.engine = knowledge_engine.engine(__file__)

    def load_knowledge(self, diseases):
        # Convert Django model data to PyKE facts
        for disease in diseases:
            self.engine.assert_('diseases', 'disease', (disease.name,))
            for symptom in disease.symptoms.all():
                self.engine.assert_('diseases', 'has_symptom', (disease.name, symptom.name))
            for treatment in disease.treatments.all():
                self.engine.assert_('diseases', 'has_treatment', (disease.name, treatment.name))
            for prevention in disease.preventions.all():
                self.engine.assert_('diseases', 'has_prevention', (disease.name, prevention.name))

    def diagnose(self, symptoms):
        self.engine.reset()
        try:
            self.engine.activate('diagnosis')
            with self.engine.prove_goal('diagnosis.diagnose($symptoms, $disease, $match_ratio)') as gen:
                for vars, plan in gen:
                    yield vars['disease'], vars['match_ratio']
        except Exception:
            krb_traceback.print_exc()
            sys.exit(1)

    def get_treatments(self, disease):
        treatments = []
        with self.engine.prove_goal('diseases.has_treatment(%s, $treatment)' % disease) as gen:
            for vars, plan in gen:
                treatments.append(vars['treatment'])
        return treatments

    def get_preventions(self, disease):
        preventions = []
        with self.engine.prove_goal('diseases.has_prevention(%s, $prevention)' % disease) as gen:
            for vars, plan in gen:
                preventions.append(vars['prevention'])
        return preventions