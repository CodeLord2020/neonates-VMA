from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.response import Response
from .expert_system import *
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


class Diagnose(APIView):
    def post(self, request, format=None):
        symptoms = request.data.get('symptoms', [])
        
        expert_system = NeonatalExpertSystem()
        diseases = Disease.objects.all()
        expert_system.load_knowledge(diseases)
        
        results = []
        for disease, match_ratio in expert_system.diagnose(symptoms):
            results.append({
                'disease': disease,
                'match_ratio': match_ratio,
                'treatments': expert_system.get_treatments(disease),
                'preventions': expert_system.get_preventions(disease),
            })
        
        results.sort(key=lambda x: x['match_ratio'], reverse=True)
        return Response(results)



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