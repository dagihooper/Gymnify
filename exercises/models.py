# models.py placeholder

from django.db import models
from django.contrib.auth.models import User


class ActivityLevel(models.Model):
    level = models.CharField(max_length=20)
    reps = models.IntegerField()
    sets = models.IntegerField()

    def __str__(self):
        return f"{self.level.capitalize()} - {self.reps} reps x {self.sets} sets"


class Alternative(models.Model):
    name = models.CharField(max_length=100)
    caloriesPerRep = models.FloatField()
    description = models.TextField()
    equipment = models.BooleanField(default=False)


class Exercise(models.Model):
    CATEGORY_CHOICES = [
        ('chest', 'Chest'),
        ('back', 'Back'),
        ('shoulders', 'Shoulders'),
        ('arms', 'Arms'),
        ('biceps', 'Biceps'),
        ('triceps', 'Triceps'),
        ('core', 'Core'),
        ('legs', 'Legs'),
    ]

    name = models.CharField(max_length=100)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    caloriesPerRep = models.FloatField()
    image = models.CharField(max_length=255)
    video = models.CharField(max_length=255)
    description = models.TextField()
    timeTaken = models.CharField(max_length=50, blank=True, null=True)
    requireKG = models.JSONField(blank=True, null = True)
    effectiveness = models.IntegerField()
    activityLevels = models.JSONField()
    equipment = models.BooleanField(default=False)
    primaryMuscles = models.JSONField()
    secondaryMuscles = models.JSONField()
    alternatives = models.ManyToManyField(Alternative)

    def __str__(self):
        return self.name
