# mealplanner/utils.py
from datetime import date
from math import floor
from .models import Food

def meal_plan(profile, userfastinglog):
    targets = calculate_targets(profile)
    qs = Food.objects.all()

    if userfastinglog.is_fasting:
        qs = qs.filter(fasting=True)
    else:
        qs = qs.filter(fasting=False)  # optional

    plan = {}

    for food in qs:
        periods = [p.name for p in food.periods.all()]
        budget = None
        daymeals = food.daymeal_set.all()
        if daymeals.exists():
            budget = daymeals.first().budget_level  # e.g., 'lowBudget', 'mediumBudget', 'highBudget'

        macros = getattr(food, 'macros', None)
        micros = getattr(food, 'micros', None)
        if not macros or not micros:
            continue

        # Optional nutrient filter (you can keep or remove this)
        if macros.protein >= 5 or micros.iron >= 3 or micros.calcium >= 100:
            food_data = {
                "food": food.food_name,
                "protein": macros.protein,
                "carbs": macros.carbs,
                "fats": macros.fats,
                "calories": macros.calories,
                "iron": micros.iron,
                "calcium": micros.calcium,
                "thiamine": micros.thiamine,
                "budget": budget
            }
            
            for period in periods:
                if period not in plan:
                    plan[period] = {}
                if budget not in plan[period]:
                    plan[period][budget] = []
                plan[period][budget].append(food_data)

    return {
        "targets": targets,
        "plan": plan
    }


def calculate_targets(profile):
  
    age = profile.age
    weight = profile.weight
    height = profile.height
    gender = profile.gender.lower()
    activity_factor_map = {
    "SA": 1.2,   
    "LA": 1.55,  
    "MA": 1.65,  
    "HA": 1.725  
                }
    activity_factor = activity_factor_map.get(profile.activityLevel, 1.2)

    if gender == "male":
        bmr = (10.00 * float(weight)) + (6.25 * float(height)) - (5.00 * float(age)) + 5
    else:
        bmr = (10.00 * float(weight)) + (6.25 * float(height)) - (5.00 * float(age)) - 161

    calories = bmr * activity_factor

    # Macronutrients
    protein_g = (0.15 * calories) / 4
    fat_g = (0.30 * calories) / 9
    carbs_g = (0.55 * calories) / 4

    # Micronutrients — base WHO values
    micros = {
        "iron": 18 if gender == "female" else 8,
        "calcium": 1000,
        "thiamine": 1.2
    }

    return {
        "calories": floor(calories),
        "protein": round(protein_g, 1),
        "fats": round(fat_g, 1),
        "carbs": round(carbs_g, 1),
        "micronutrients": micros
    }
