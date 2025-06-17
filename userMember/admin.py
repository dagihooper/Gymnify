from django.contrib import admin
from .models import UserProfile


class UserProfileAdmin(admin.ModelAdmin):
  list_display = ('user','gym_house', 'first_name', 'last_name', 'email', 'phone_number', 'age', 'weight', 'height', 'gender', 'exercise_day', 'health_status', 'exercise_type', 'blood_type', 'exercise_time_per_day', 'fitness_goal' ,'profile_photo', 'phone_verified' )

from allauth.socialaccount.models import SocialApp
from django.contrib.sites.models import Site

site = Site.objects.get(id=1)

google_app = SocialApp.objects.create(
    provider="google",
    name="Google",
    client_id="1066412862720-s6dkda63hp3l7j0lrie38ff7a7quj57b.apps.googleusercontent.com",
    secret="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",
)
google_app.sites.add(site)

admin.site.register(UserProfile, UserProfileAdmin)
