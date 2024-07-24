from django.db import models

# Create your models here.

from django.db import models


class Disease(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self) -> str:
        return self.name


class Symptom(models.Model):
    name = models.CharField(max_length=100)
    diseases = models.ManyToManyField(Disease, related_name='symptoms')

    def __str__(self) -> str:
        return self.name


class Diagnosis(models.Model):
    name = models.CharField(max_length=100)
    diseases = models.ManyToManyField(Disease, related_name='diagnoses')
 
    def __str__(self) -> str:
        return self.name


class Treatment(models.Model):
    name = models.CharField(max_length=100)
    diseases = models.ManyToManyField(Disease, related_name='treatments')

    def __str__(self) -> str:
        return self.name
    

class Prevention(models.Model):
    name = models.CharField(max_length=100)
    diseases = models.ManyToManyField(Disease, related_name='preventions')

    def __str__(self) -> str:
        return self.name

    diseases = models.ManyToManyField(Disease, related_name='preventions')




class ApgarScore(models.Model):
    APPEARANCE_CHOICES = [
        ('All blue pale', 'All blue pale'),
        ('Pink body, blue extremities', 'Pink body, blue extremities'),
        ('All pink', 'All pink'),
    ]
    PULSE_CHOICES = [
        ('No Pulse', 'No Pulse'),
        ('Less than 100', 'Less than 100'),
        ('More than 100', 'More than 100'),
    ]
    GRIMACE_CHOICES = [
        ('No response', 'No response'),
        ('Grimace', 'Grimace'),
        ('Sneeze, Cough', 'Sneeze, Cough'),
    ]
    ACTIVITY_CHOICES = [
        ('Limp', 'Limp'),
        ('Some flexion', 'Some flexion'),
        ('Active movement', 'Active movement'),
    ]
    RESPIRATION_CHOICES = [
        ('Absent', 'Absent'),
        ('Weak cry', 'Weak cry'),
        ('Good cry', 'Good cry'),
    ]

    appearance = models.CharField(max_length=50, choices=APPEARANCE_CHOICES)
    pulse = models.CharField(max_length=50, choices=PULSE_CHOICES)
    grimace = models.CharField(max_length=50, choices=GRIMACE_CHOICES)
    activity = models.CharField(max_length=50, choices=ACTIVITY_CHOICES)
    respiration = models.CharField(max_length=50, choices=RESPIRATION_CHOICES)