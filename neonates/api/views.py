from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import *
# Create your views here.

class DiseaseList(generics.ListAPIView):
    queryset = Disease.objects.all()
    serializer_class = DiseaseSerializer

class DiseaseDetail(generics.RetrieveAPIView):
    queryset = Disease.objects.all()
    serializer_class = DiseaseSerializer

class SymptomList(generics.ListAPIView):
    queryset = Symptom.objects.all()
    serializer_class = SymptomSerializer

class SymptomDetail(generics.RetrieveAPIView):
    queryset = Symptom.objects.all()
    serializer_class = SymptomSerializer



# def HomeView(request):
#     return render (request, template_name='home.html')

# def Home1View(request):
#     return render (request, template_name='home1.html')

def IndexView(request):
    return render (request, template_name='index.html')





class Diagnose(APIView):
    def post(self, request, format=None):
        payload_symptoms = set(request.data.get('symptoms', []))
        
        # Get all diseases that have at least one symptom in the payload
        diseases = Disease.objects.filter(symptoms__name__in=payload_symptoms).distinct()
        
        disease_descriptions = {
        "Birth Asphyxia": "A decrease in blood flow to a newborn's tissues or oxygen in their blood before, during, or just after delivery.",
        "RDS": "Primarily seen in premature infants due to a deficiency in surfactant, a substance that keeps the alveoli in the lungs open.",
        "Neonatal Pneumonia": "Lung infection in a newborn. Onset may be within hours of birth or after 7 days."}

        results = []
        
        for disease in diseases:
            disease_symptoms = set(disease.symptoms.values_list('name', flat=True))
            matched_symptoms = disease_symptoms.intersection(payload_symptoms)
            
            # Calculate percentage fit
            percentage_fit = (len(matched_symptoms) / len(disease_symptoms)) * 100
            description = disease_descriptions.get(disease.name)
            
            results.append({
                'disease': disease.name,
                'description': description,
                'percentage_fit': round(percentage_fit, 2),
                'matched_symptoms': list(matched_symptoms),
                'treatments': [t.name for t in disease.treatments.all()],
                'preventions': [p.name for p in disease.preventions.all()],
            })
            

        # Sort results by percentage fit in descending order
        results.sort(key=lambda x: x['percentage_fit'], reverse=True)
        
        return Response(results)


# class Diagnose(APIView):
#     def post(self, request, format=None):
#         symptoms = request.data.get('symptoms', [])
#         diseases = Disease.objects.filter(symptoms__name__in=symptoms).distinct()
        
#         results = []
#         for disease in diseases:
#             matched_symptoms = disease.symptoms.filter(name__in=symptoms)
#             match_ratio = len(matched_symptoms) / disease.symptoms.count()
#             results.append({
#                 'disease': disease.name,
#                 'match_ratio': match_ratio,
#                 'matched_symptoms': [s.name for s in matched_symptoms],
#                 'treatments': [t.name for t in disease.treatments.all()],
#                 'preventions': [p.name for p in disease.preventions.all()],
#             })
        
#         results.sort(key=lambda x: x['match_ratio'], reverse=True)
#         return Response(results)
    

# class CalculateApgar(APIView):
#     def post(self, request, format=None):
#         scores = {
#             'appearance': {'All blue pale': 0, 'Pink body, blue extremities': 1, 'All pink': 2},
#             'pulse': {'No Pulse': 0, 'Less than 100': 1, 'More than 100': 2},
#             'grimace': {'No response': 0, 'Grimace': 1, 'Sneeze, Cough': 2},
#             'activity': {'Limp': 0, 'Some flexion': 1, 'Active movement': 2},
#             'respiration': {'Absent': 0, 'Weak cry': 1, 'Good cry': 2}
#         }

#         try:
#             total_score = sum(scores[k][v] for k, v in request.data.items())
#         except KeyError:
#             return Response({"error": "Invalid input. Please provide all required Apgar score components."}, 
#                             status=status.HTTP_400_BAD_REQUEST)
        
#         assessment = "Normal" if total_score >= 7 else "Intermediate" if 4 <= total_score <= 6 else "Low"
#         action = ("No immediate action required." if assessment == "Normal" else
#                   "Close monitoring required." if assessment == "Intermediate" else
#                   "Immediate medical intervention required.")
        
#         return Response({
#             'score': total_score,
#             'assessment': assessment,
#             'action': action
#         })
    

class CalculateApgar(APIView):
    def post(self, request, format=None):
        serializer = ApgarScoreSerializer(data=request.data)
        if serializer.is_valid():
            scores = {
                'appearance': {'All blue pale': 0, 'Pink body, blue extremities': 1, 'All pink': 2},
                'pulse': {'No Pulse': 0, 'Less than 100': 1, 'More than 100': 2},
                'grimace': {'No response': 0, 'Grimace': 1, 'Sneeze, Cough': 2},
                'activity': {'Limp': 0, 'Some flexion': 1, 'Active movement': 2},
                'respiration': {'Absent': 0, 'Weak cry': 1, 'Good cry': 2}
            }

            total_score = sum(scores[k][v] for k, v in serializer.validated_data.items())
            
            assessment = "Normal" if total_score >= 7 else "Intermediate" if 4 <= total_score <= 6 else "Low"
            action = ("No immediate action required." if assessment == "Normal" else
                      "Close monitoring required." if assessment == "Intermediate" else
                      "Immediate medical intervention required.")
            
            return Response({
                'score': total_score,
                'assessment': assessment,
                'action': action
            })
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ApgarChoices(APIView):
    def get(self, request, format=None):
        return Response({
            'appearance': dict(ApgarScore.APPEARANCE_CHOICES),
            'pulse': dict(ApgarScore.PULSE_CHOICES),
            'grimace': dict(ApgarScore.GRIMACE_CHOICES),
            'activity': dict(ApgarScore.ACTIVITY_CHOICES),
            'respiration': dict(ApgarScore.RESPIRATION_CHOICES),
        })