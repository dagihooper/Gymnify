from django.contrib import admin
from .models import Period, Goal, Food, Macronutrients, Micronutrients, DayMeal

@admin.register(Food)
class FoodAdmin(admin.ModelAdmin):
    list_display = ('food_name', 'food_type', 'scaling_type', 'popularity', 'availability', 'halal', 'fasting', 'min_portion', 'max_portion')
    list_filter = ('halal', 'fasting', 'food_type', 'availability')
    search_fields = ('food_name',)
    filter_horizontal = ('periods', 'goals')  # ManyToMany admin widget

@admin.register(Period)
class PeriodAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(Goal)
class GoalAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(Macronutrients)
class MacronutrientsAdmin(admin.ModelAdmin):
    list_display = ('food', 'protein', 'carbs', 'fats', 'calories')

@admin.register(Micronutrients)
class MicronutrientsAdmin(admin.ModelAdmin):
    list_display = ('food', 'iron', 'calcium', 'thiamine')

@admin.register(DayMeal)
class DayMealAdmin(admin.ModelAdmin):
    list_display = ('day', 'budget_level', 'period', 'food')
