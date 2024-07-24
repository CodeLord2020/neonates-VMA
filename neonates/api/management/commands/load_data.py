import json
from django.core.management.base import BaseCommand
from api.models import Disease, Symptom, Diagnosis, Treatment, Prevention

class Command(BaseCommand):
    help = 'Load disease data from JSON'

    def handle(self, *args, **kwargs):
        with open('neonatal_knowledge_base.json', 'r') as f:
            data = json.load(f)

        for disease_name, disease_data in data.items():
            disease, _ = Disease.objects.get_or_create(name=disease_name)

            for symptom_name in disease_data['symptoms']:
                symptom, _ = Symptom.objects.get_or_create(name=symptom_name)
                disease.symptoms.add(symptom)

            for diagnosis_name in disease_data['diagnosis']:
                diagnosis, _ = Diagnosis.objects.get_or_create(name=diagnosis_name)
                disease.diagnoses.add(diagnosis)

            for treatment_name in disease_data['treatment']:
                treatment, _ = Treatment.objects.get_or_create(name=treatment_name)
                disease.treatments.add(treatment)

            for prevention_name in disease_data['prevention']:
                prevention, _ = Prevention.objects.get_or_create(name=prevention_name)
                disease.preventions.add(prevention)

        self.stdout.write(self.style.SUCCESS('Successfully loaded disease data'))