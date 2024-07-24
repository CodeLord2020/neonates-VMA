from rest_framework import serializers
from .models import Disease, Symptom, Diagnosis, Treatment, Prevention, ApgarScore



class DiseaseSerializer(serializers.ModelSerializer):
    symptoms = serializers.StringRelatedField(many=True)
    diagnoses = serializers.StringRelatedField(many=True)
    treatments = serializers.StringRelatedField(many=True)
    preventions = serializers.StringRelatedField(many=True)

    class Meta:
        model = Disease
        fields = ['id', 'name', 'symptoms', 'diagnoses', 'treatments', 'preventions']



class SymptomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Symptom
        fields = ['id', 'name']



class ApgarScoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = ApgarScore
        fields = ['appearance', 'pulse', 'grimace', 'activity','respiration']