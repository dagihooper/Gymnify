# mealplanner/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from pymongo import MongoClient
from .models import Food
from Gymnify.mongo_utils import get_foods_collection

@receiver(post_save, sender=Food)
def sync_food_to_mongo(sender, instance, created, **kwargs):
    print(f"\n🔔 Signal triggered for Food: {instance.food_name}")
    print(f"   - Was it newly created? {created}")
    print("   - Syncing data to MongoDB...")

    food_collection = get_foods_collection()

    # Convert M2M fields (periods and goals) into lists
    periods = list(instance.periods.values_list('name', flat=True))
    goals = list(instance.goals.values_list('name', flat=True))

    # Include macronutrients
    macros = {}
    if hasattr(instance, 'macros'):
        macros = {
            "protein": instance.macros.protein,
            "carbs": instance.macros.carbs,
            "fats": instance.macros.fats,
            "calories": instance.macros.calories,
        }

    # Include micronutrients
    micros = {}
    if hasattr(instance, 'micros'):
        micros = {
            "iron": instance.micros.iron,
            "calcium": instance.micros.calcium,
            "thiamine": instance.micros.thiamine,
        }

    # Build the full food document
    food_data = {
        "food_name": instance.food_name,
        "description": instance.description,
        "food_type": instance.food_type,
        "scaling_type": instance.scaling_type,
        "ingredients": instance.ingredients,
        "combine_with": instance.combine_with,
        "not_combine_with": instance.not_combine_with,
        "popularity": instance.popularity,
        "availability": instance.availability,
        "halal": instance.halal,
        "fasting": instance.fasting,
        "min_portion": instance.min_portion,
        "max_portion": instance.max_portion,
        "periods": periods,
        "goals": goals,
        "macronutrients": macros,
        "micronutrients": micros,
    }

    # Use food_name as unique key (or use instance.id if better)
    food_collection.update_one(
        {"food_name": instance.food_name},
        {"$set": food_data},
        upsert=True
    )
