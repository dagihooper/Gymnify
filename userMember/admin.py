from django.contrib import admin
from .models import UserProfile


class UserProfileAdmin(admin.ModelAdmin):
  list_display = ('user','gym_house', 'first_name', 'last_name', 'email', 'phone_number', 'age', 'weight', 'height', 'gender', 'exercise_day', 'health_status', 'exercise_type', 'blood_type', 'exercise_time_per_day', 'fitness_goal' ,'profile_photo', 'phone_verified' )

  

admin.site.register(UserProfile, UserProfileAdmin)
