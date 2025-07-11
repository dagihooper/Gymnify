from django.shortcuts import render, redirect
from Gymnify.mongo_utils import get_gymers_collection
from django.contrib import messages
from userMember.models import UserProfile
from django.contrib.auth.models import User
from allauth.socialaccount.models import SocialAccount
import requests
from django.conf import settings
from .utils import send_verification_code
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime


def insertion(request):
  
  gymers_collection = get_gymers_collection()
  gym_house = request.session.get('gym_house', '')
  username = request.session.get('username', '')
  user = request.user
  
  if not username:
    
    messages.error(request, 'You need to register first')
    return redirect('register')
  
  user = User.objects.filter(username=username).first()
  profile = UserProfile.objects.filter(user = user).first()
  gymers  = list(gymers_collection.find())
  
  if SocialAccount.objects.filter(user=user).exists():
      profile = UserProfile.objects.filter(email = request.user.email).first()
      if profile:
        first_name = profile.first_name
        last_name = profile.last_name
        request.session['first_name'] = first_name
        request.session['last_name'] = last_name
        
  if profile:
      first_name = profile.first_name
      last_name = profile.last_name
      
  context = {
    'first_name': first_name,
    'last_name': last_name,
    'gymers': gymers,
    'gym_house': gym_house
    
  }
  
  if context['gym_house']:
    request.session['gym_house'] = gym_house
    
  if request.method == 'POST':
    
    phone_number = request.POST.get('phone_number')
    gym_house = request.POST.get('gym_house')
    phone_number = f"0{phone_number}" 
    phone_number_exist = UserProfile.objects.filter(phone_number = phone_number).exists()
        
    if gym_house:
        registeredDate = datetime.now().strftime("%Y, %m, %d")

        
        new_user_mongo = {
              "userName": username,
              "firstName": profile.first_name,
              "lastName": profile.last_name,
              "phoneVerified": False,
              "email": request.user.email,
              "phone" : '',
              "age": '',
              "sex": '',
              "height": '',
              "weight": '',
              "registeredDate": registeredDate,
              "paymentDate": '',
              "exerciseTimePerDay": '',
              "notificationTime": '',
              "healthStatus": '',
              "exerciseType" : '',
              "enteringTime": '',
              "bloodType" : '',
              "upComingExercise": '',
              "totalTimeSpendOnGym": '',
              'protienAmountRequired': '',
              "TodayNotification": '',
              "activityLevel": '',
              "fitnessGoal": '',
            }
        
        gymers_collection.update_one({
          'name': gym_house
        }, {"$push": {
          'users': new_user_mongo
        }})
      
    if not phone_number_exist and user:

      profile= UserProfile.objects.get(user = user)
      profile.phone_number = f"{phone_number}"
      if gym_house:
        profile.gym_house = gym_house
      
      gymers_collection.update_one(
      {"users.userName": username},
      {"$set": { "users.$.phone": phone_number}}
    )
      gymers = list(gymers_collection.find({'users.username': 'step'}))
      for gymer in gymers:
           pass      
      
      
      phone_number = profile.phone_number[1:]
      request.session['phone_number'] = phone_number
      profile.save()    
      result = send_verification_code()
      
      if result['status'] == 'success':
        return redirect(result['redirect'])
      elif result['status'] == 'error':
       print('API error:', result['message'])
      else:
        print(f"HTTP error ... code: {result['code']}, msg: {result['message']}")
    
    else:
      messages.error(request, 'The phone number has already taken choose another one.')  
  else:
    pass  
  request.session['username'] = username
    
  return render(request, 'insertion.html', context)
      
  
def validation(request):
  gymers_collection = get_gymers_collection()
  
  username = request.session.get('username', '') 
  user = User.objects.filter(username=username).first()
  user_profile= UserProfile.objects.filter(user = user).first()
  
  phone_number = request.session.get('phone_number')  

  if phone_number:
    if request.method == 'POST':
                  
      entered_otp = request.POST.get('otp').strip()
      session = requests.Session()
      base_url = 'https://api.afromessage.com/api/verify'
      token = 'eyJhbGciOiJIUzI1NiJ9.eyJpZGVudGlmaWVyIjoidkc4ZUZacm55eW1xbDVMQ3VSVEZwRmlRZUxhNmhxVnoiLCJleHAiOjE5MTAwMTI4NTUsImlhdCI6MTc1MjI0NjQ1NSwianRpIjoiN2ZkZmUyZWMtMGUwYS00YTNiLWIyNjgtYTYzZDk1NmE1YWU4In0.cx3izFES9LXG_LfSOf0jCa0USP9zl1iacbrAL29Sr44'
      headers = {'Authorization': 'Bearer ' + token}
      to = '+251970758542'
      code = entered_otp

      url = '%s?to=%s&code=%s' % (base_url, to, code)
      result = session.get(url, headers=headers)
      if result.status_code == 200:
          json = result.json()
          if json['acknowledge'] == 'success':
              messages.success(request, 'You are succesfully signed in.')
              user_profile.phone_verified = True
              gymers_collection.update_one (
                {'users.userName': username},
                {'$set': {'users.$.phoneVerified': True}}
              )
              user_profile.save()
              
              return redirect('login')
          else:
              messages.error(request, 'The otp you entered is incorrect, try again')

      else:
          print('HTTP error ... code: %d, msg: %s' % (result.status_code, result.content))
     

    return render(request, 'validation.html', {'phone_number': phone_number})
  
  else:
    messages.error(request, 'Please first complete the phone number page.' ) 
    return redirect('register')
  
  
  
def custom_403_view(request, reason=""):
    return render(request, '403.html', {"reason": reason}, status=403)


@csrf_exempt
def resend_otp(request):
  if request.method == 'POST':
    phone_number = request.session.get('phone_number')
    
    result = send_verification_code()
      
    if result['status'] == 'success':
      return redirect(result['redirect'])
    elif result['status'] == 'error':
      print('API error:', result['message'])
    else:
      print(f"HTTP error ... code: {result['code']}, msg: {result['message']}")
    


