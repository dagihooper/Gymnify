# exercises/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Exercise
from Gymnify.mongo_utils import get_exercises_collection


@receiver(post_save, sender=Exercise)
def sync_exercise_to_mongo(sender, instance, created, **kwargs):
    exercise_collection = get_exercises_collection()

    # Get related alternatives as list of dicts (or just names)
    alternatives = list(instance.alternatives.values('id', 'name', 'caloriesPerRep', 'equipment'))

    exercise_data = {
        "name": instance.name,
        "category": instance.category,
        "caloriesPerRep": instance.caloriesPerRep,
        "image": instance.image,
        "video": instance.video,
        "description": instance.description,
        "timeTaken": instance.timeTaken,
        "requireKG": instance.requireKG,
        "effectiveness": instance.effectiveness,
        "activityLevels": instance.activityLevels,
        "equipment": instance.equipment,
        "primaryMuscles": instance.primaryMuscles,
        "secondaryMuscles": instance.secondaryMuscles,
        "alternatives": alternatives,
    }

    exercise_collection.update_one(
        {"_id": str(instance.pk)},  # Use the Exercise PK as unique Mongo _id
        {"$set": exercise_data},
        upsert=True
    )
