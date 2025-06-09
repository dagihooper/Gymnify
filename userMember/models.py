from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model



class UserProfile(models.Model):
  user = models.OneToOneField(User, on_delete=models.CASCADE) 
  first_name = models.CharField(max_length=30, null=True, blank=True)
  last_name = models.CharField(max_length=30, null=True, blank=True)
  email = models.EmailField(max_length=254, null=True, blank=True)
  phone_number = models.CharField(max_length= 35, null= True, )
  gym_house = models.CharField(max_length=30, null= True)
  age = models.IntegerField(blank= True, null=True )
  profile_photo = models.ImageField(upload_to = '', null= True)
  weight = models.DecimalField(max_digits = 6, decimal_places = 2, null = True )
  height = models.CharField(max_length  = 3, null= True)
  gender = models.CharField(max_length = 10, choices= [('M', 'Male'), ('F', 'Female')], default='M', null = True, blank = True)
  exercise_day = models.IntegerField(blank = True, null = True)
  health_status = models.CharField(max_length= 10, null = True)
  exercise_type = models.CharField(max_length = 20, null = True)
  blood_type = models.CharField(max_length = 20, null = True)
  exercise_time_per_day = models.CharField(max_length=30, null=True )
  fitness_goal = models.CharField(max_length=30, null= True)
  phone_verified = models.BooleanField(default=False)
  notificationTime = models.CharField(max_length=30, null = True)
  enteringTime = models.CharField(max_length=30, null = True)
  totalTimeSpendOnGym = models.CharField(max_length=30, null = True)
  activityLevel = models.CharField(max_length=10, choices = [('SL', 'Sedentary Level'), ('LA', 'Light Active'), ('MA', 'Moderately Active'), ('VA', 'Very Active')], default= 'LA', null = True, blank = True )
  

  def __str__(self):
        return f"{self.user.username}'s Profile"
      
