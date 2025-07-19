import json
from django.core.management.base import BaseCommand
from exercises.models import Exercise, Alternative


class Command(BaseCommand):
    help = "Load exercises from JSON"

    def handle(self, *args, **kwargs):
        with open('exercises.json', 'r') as file:
            data = json.load(file)

        for category, exercises in data.items():
            for ex in exercises:
                # Create or get exercise
                exercise = Exercise.objects.create(
                    name=ex['name'],
                    category=category,
                    caloriesPerRep=ex['caloriesPerRep'],
                    image=ex['image'],
                    video=ex['video'],
                    description=ex['description'],
                    timeTaken=ex.get('timeTaken', ''),
                    requireKG=ex.get('requireKG', {}),
                    effectiveness=ex['effectiveness'],
                    activityLevels=ex['activityLevels'],
                    equipment=ex['equipment'],
                    primaryMuscles=ex['primaryMuscles'],
                    secondaryMuscles=ex['secondaryMuscles']
                )

                # Create alternatives
                for alt in ex.get('alternatives', []):
                    alt_obj, _ = Alternative.objects.get_or_create(
                        name=alt['name'],
                        defaults={
                            'caloriesPerRep': alt['caloriesPerRep'],
                            'description': alt['description'],
                            'equipment': alt['equipment']
                        }
                    )
                    exercise.alternatives.add(alt_obj)

                self.stdout.write(self.style.SUCCESS(f"✔ Loaded: {exercise.name}"))

        