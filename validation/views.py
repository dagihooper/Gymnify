from django.shortcuts import render, redirect
import json
import qrcode
import base64
from io import BytesIO
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
        full_name = profile.full_name
        request.session['full_name'] = full_name
        
  if profile:
      full_name = profile.full_name
      
  context = {
    'full_name': full_name,
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
        

        
        # new_user_mongo = {
        #       "userName": username,
        #       "phoneVerified": False,
        #       "email": request.user.email,
        #       "phone" : '',
        #       "age": '',
        #       "sex": '',
        #       "height": '',
        #       "weight": '',
        #       "registeredDate": registeredDate,
        #       "paymentDate": '',
        #       "exerciseTimePerDay": '',
        #       "notificationTime": '',
        #       "healthStatus": '',
        #       "exerciseType" : '',
        #       "enteringTime": '',
        #       "bloodType" : '',
        #       "upComingExercise": '',
        #       "totalTimeSpendOnGym": '',
        #       'protienAmountRequired': '',
        #       "TodayNotification": '',
        #       "activityLevel": '',
        #       "fitnessGoal": '',
        #     }
        
        # gymers_collection.update_one({
        #   'name': gym_house
        # }, {"$push": {
        #   'users': new_user_mongo
        # }})
      
    if not phone_number_exist and user:

      profile.phone_number = f"{phone_number}"
      if gym_house:
        profile.gym_house = gym_house
      
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
      to = '+251963719303'
      code = entered_otp

      url = '%s?to=%s&code=%s' % (base_url, to, code)
      result = session.get(url, headers=headers)
      if result.status_code == 200:
          response_json = result.json()
          if response_json['acknowledge'] == 'success':
              messages.success(request, 'You are succesfully signed in.')
              user_profile.phone_verified = True
              registeredDate = datetime.now().strftime("%Y, %m, %d")

              user_data = {
                  "name": username,
                  "email": user_profile.email,
                  "phone": user_profile.phone_number
              }

              json_data = json.dumps(user_data)
              qr = qrcode.QRCode(
                  version=1,
                  error_correction=qrcode.constants.ERROR_CORRECT_L,
                  box_size=10,
                  border=4,
              )
              qr.add_data(json_data)
              qr.make(fit=True)

              img = qr.make_image(fill_color="black", back_color="white")
              buffer = BytesIO()
              img.save(buffer, format="PNG")
              img_base64 = base64.b64encode(buffer.getvalue()).decode("utf-8")
              user_profile.qr_code = f'data:image/png;base64,{img_base64}'


              # gymers_collection.update_one (
              #   {'users.userName': username},
              #   {'$set': {'users.$.phoneVerified': True}}
              # )
               


            
              new_user_mongo = {
                  "userName": username,
                  "fullName": user_profile.full_name,
                  "phoneVerified": True,
                  "email": request.user.email,
                  "password": user.password,
                  "phone" : user_profile.phone_number,
                  "age": '',
                  "qrCode": img_base64,
                  "profilePhoto": '',
                  "sex": '',
                  "height": '',
                  "weight": '',
                  "registeredDate": registeredDate,
                  "paymentDate": '',
                  "paymentStatus": False,
                  "exerciseTimePerDay": '',
                  "notificationTime": '',
                  "healthStatus": '',
                  "exerciseType" : '',
                  "enteringTime": '',
                  "bloodType" : '',
                  "exercise": [],
                  "upComingExercise": '',
                  "totalTimeSpendOnGym": '',
                  'protienAmountRequired': '',
                  "TodayNotification": '',
                  "activityLevel": '',
                  "fitnessGoal": '',
                }
            
              gymers_collection.update_one({
                'name': user_profile.gym_house
              }, {"$push": {
                'users': new_user_mongo
              }})

              user_profile.save()
              
              return redirect('home')
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
    


