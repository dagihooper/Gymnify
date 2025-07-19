# admin.py placeholder
from django.contrib import admin
from .models import Exercise, Alternative, ActivityLevel

@admin.register(Exercise)

class ExerciseAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'caloriesPerRep')

admin.site.register(Alternative)
admin.site.register(ActivityLevel)