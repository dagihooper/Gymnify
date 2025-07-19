import json
from django.core.management.base import BaseCommand
from mealplanner.models import Food, Macronutrients, Micronutrients, Period, Goal, DayMeal

class Command(BaseCommand):
    help = "Load meals from JSON"

    def handle(self, *args, **kwargs):
        with open('Foods.json') as f:
            data = json.load(f)

        for day_key, day_val in data.items():
            for period_name, budget_dict in day_val.items():
                period_obj, _ = Period.objects.get_or_create(name=period_name)

                for budget, foods in budget_dict.items():
                    for food in foods:
                        food_obj, _ = Food.objects.get_or_create(
                            food_name=food['foodName'],
                            defaults={
                                'description': food['description'],
                                'food_type': food['foodType'],
                                'scaling_type': food['scalingType'],
                                'ingredients': food['ingredients'],
                                'combine_with': food['combineWith'],
                                'not_combine_with': food['notCombineWith'],
                                'popularity': food['popularity'],
                                'availability': food['availability'],
                                'halal': food['halal'],
                                'fasting': food['fasting'],
                                'min_portion': food['minMaxPortion'][0],
                                'max_portion': food['minMaxPortion'][1],
                            }
                        )
                        food_obj.periods.add(*[Period.objects.get_or_create(name=p)[0] for p in food['period']])
                        food_obj.goals.add(*[Goal.objects.get_or_create(name=g)[0] for g in food['forGoalOf']])

                        Macronutrients.objects.update_or_create(
                            food=food_obj,
                            defaults=food['macrosPerScalingType']
                        )
                        Micronutrients.objects.update_or_create(
                            food=food_obj,
                            defaults=food['micronutrientsPerScalingType']
                        )

                        DayMeal.objects.get_or_create(
                            day=day_key,
                            budget_level=budget,
                            period=period_obj,
                            food=food_obj
                        )

        self.stdout.write(self.style.SUCCESS("Meals loaded successfully."))
