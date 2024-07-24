from django.urls import path
from .views import *
urlpatterns = [
    path('diseases/', DiseaseList.as_view(), name='disease-list'),
    path('diseases/<int:pk>/', DiseaseDetail.as_view(), name='disease-detail'),
    path('symptoms/', SymptomList.as_view(), name='symptom-list'),
    path('symptoms/<int:pk>/', SymptomDetail.as_view(), name='symptom-detail'),
    path('diagnose/', Diagnose.as_view(), name='diagnose'),
    path('get-apgar-parameters/', ApgarChoices.as_view(), name='get-apgar-parameters'),
    path('calculate-apgar/', CalculateApgar.as_view(), name='calculate-apgar'),
]