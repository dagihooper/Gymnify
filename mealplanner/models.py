# mealplanner/models.py

from django.db import models

class Period(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

class Goal(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

class Food(models.Model):
    food_name = models.CharField(max_length=100)
    description = models.TextField()
    food_type = models.CharField(max_length=50)
    scaling_type = models.CharField(max_length=50)
    ingredients = models.JSONField()
    combine_with = models.JSONField()
    not_combine_with = models.JSONField()
    popularity = models.CharField(max_length=10)
    availability = models.CharField(max_length=10)
    halal = models.BooleanField()
    fasting = models.BooleanField()
    min_portion = models.IntegerField()
    max_portion = models.IntegerField()

    periods = models.ManyToManyField(Period)
    goals = models.ManyToManyField(Goal)

    def __str__(self):
        return self.food_name

class Macronutrients(models.Model):
    food = models.OneToOneField(Food, on_delete=models.CASCADE, related_name='macros')
    protein = models.FloatField()
    carbs = models.FloatField()
    fats = models.FloatField()
    calories = models.FloatField()

class Micronutrients(models.Model):
    food = models.OneToOneField(Food, on_delete=models.CASCADE, related_name='micros')
    iron = models.FloatField()
    calcium = models.FloatField()
    thiamine = models.FloatField()

class DayMeal(models.Model):
    day = models.CharField(max_length=10)
    budget_level = models.CharField(max_length=20)
    period = models.ForeignKey(Period, on_delete=models.CASCADE)
    food = models.ForeignKey(Food, on_delete=models.CASCADE)
