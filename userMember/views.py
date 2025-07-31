from django.shortcuts import render, redirect
from Gymnify.mongo_utils import get_gymers_collection
from django.contrib.auth.models import User
from .models import UserProfile
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.db.models import Q
from datetime import datetime
import requests
from django.contrib.auth.hashers import make_password
from django.core.exceptions import ObjectDoesNotExist
from .utils import send_verification_code

def user_register(request):
    
    users_without_phone = UserProfile.objects.filter(Q(phone_number__isnull = True) | Q(gym_house__isnull = True))
    
    for users_profile in users_without_phone:
      
      user = users_profile.user
      users_profile.delete()
      user.delete()
    
    gymers_collection = get_gymers_collection()
    gymers = list(gymers_collection.find())
    
    # gymers_collection.update_many(
    #     {"$or": [
    #             {'users.phone': ''},  
    #             {'users.phoneVerified': False} 
    #         ]
    #     },
    #     {"$pull": {
    #             'users': {
    #                 "$or": [
    #                     {'phone': ''}, 
    #                     {'phoneVerified': False} 
    #                       ]}}})
        
    context = {
      'gymers': gymers
    }
  
      
    if request.method == 'POST':
        username = request.POST.get('username', '').strip().lower()
        full_name = request.POST.get('full_name', '').strip()
        registeredDate = datetime.now().strftime("%d, %m, %Y")
        password = request.POST.get('password', '').strip()
        gym_house = request.POST.get('gym_house', '').strip()
        confirm_password = request.POST.get('confirm_password', '').strip()


        if User.objects.filter(username = username).exists():
            messages.error(request, 'The username already exists')
            return redirect('register')
          
        elif not password:
            messages.error(request, 'Please insert your password.')
          
        elif password != confirm_password:
           messages.error(request, "Password doesn't match.")
           
        elif len(password) !=4 or not password.isdigit():
           messages.error(request, 'Password must be a 4-digit number')
        
        else:
     
          user = User.objects.create(username=username)
          user.set_password(password)
          user_profile = UserProfile(user=user, full_name= full_name, gym_house = gym_house)
          user.save()
          user_profile.save()

          user = authenticate(request, username = username, password= password)

          request.session['full_name'] = full_name
          request.session['username'] = username
          request.session['gym_house'] = gym_house
          
          # new_user_mongo = {
          #    "userName": username,
          #    "password": make_password(password),
          #    "phoneVerified": False,
          #    "email": '',
          #    "phone" : '',
          #    "age": '',
          #    "sex": '',
          #    "height": '',
          #    "weight": '',
          #    "registeredDate": registeredDate,
          #    "paymentDate": '',
          #    "exerciseTimePerDay": '',
          #    "notificationTime": '',
          #    "healthStatus": '',
          #    "exerciseType" : '',
          #    "enteringTime": '',
          #    "bloodType" : '',
          #    "upComingExercise": '',
          #    "totalTimeSpendOnGym": '',
          #    'protienAmountRequired': '',
          #    "TodayNotification": '',
          #    "activityLevel": '',
          #    "fitnessGoal": '',
          # }
          
        
          # gymers_collection.update_one(
          #      {'name': gym_house},
          #      {"$push": {
          #        "users": new_user_mongo
          #      }}
          #     )
            
          
    

          messages.success(request, 'You are registered successfully.')
          return redirect('insertion')  

    return render(request, 'Register.html', context )

def user_login(request):
    gymers = get_gymers_collection().find({})

    users_without_phone = UserProfile.objects.filter(Q(phone_number__isnull=True) | Q(gym_house__isnull=True))
    for users_profile in users_without_phone:
        user = users_profile.user
        users_profile.delete()
        user.delete()

    if request.method == 'POST':
        userphone = request.POST.get('userphone', '').strip().lower()
        password = request.POST.get('password')

        try:
            if userphone.startswith('09'):
                user = User.objects.get(userprofile__phone_number=userphone)
            else:
                user = User.objects.get(username=userphone)

            user = authenticate(request, username=user.username, password=password)
            if user is not None:
                login(request, user)
                request.session['userphone'] = userphone
                request.session['full_name'] = user.userprofile.full_name
                request.session['username'] = user.username
                request.session['gym_house'] = user.userprofile.gym_house
                return redirect('home')
            else:
                messages.error(request, 'Invalid Password. Please try again')

        except User.DoesNotExist:
            for gymer in gymers:
                for mongo_user in gymer.get('users', []):
                    user_name = mongo_user.get('userName', '').lower()
                    phone_number = mongo_user.get('phone', '')
                    mongo_user_password = mongo_user.get('password', '')
                    print(f'this is mongo user {user_name}')
                    print(f'this is the inputed username {userphone}')
                    print(f'this is the mongo user password {mongo_user_password}')
                    print(f'this is the password entered {password}')
                    if userphone == user_name or userphone == phone_numberp:
                        if mongo_user_password == password:
                          try:
                              user = User.objects.get(username=user_name)
                              print(f'this is a userphone {userphone}')
                          except User.DoesNotExist:
                              
                              phone_number = mongo_user.get('phone', '')
                              full_name = mongo_user.get('fullName', '')
                              gym_house = gymer.get('name', '')
                              email = mongo_user.get('email', '')
                              age = mongo_user.get('age', '')
                              weight = mongo_user.get('weight', '')
                              gender = mongo_user.get('sex', '')
                              phone_verified = mongo_user.get('phoneVerified', False)
                              # password_hash = mongo_user.get('password', '') 
                              exercise_time_per_day = mongo_user.get('exerciseTimePerDay', '')
                              blood_type = mongo_user.get('bloodType', '')
                              exercise_type = mongo_user.get('exerciseType', '')
                              fitness_goal = mongo_user.get('fitness_goal', '')
                              qr_code = mongo_user.get('qrCode', '')

                              user = User.objects.create(username=user_name, email=email)
                              user.set_password(password)

                              user_profile = UserProfile(
                                  user=user,
                                  full_name=full_name,
                                  gym_house=gym_house,
                                  email = email,
                                  phone_number=phone_number,
                                  phone_verified=phone_verified,
                                  weight=weight,
                                  age=age,
                                  gender=gender,
                                  exercise_time_per_day=exercise_time_per_day,
                                  blood_type=blood_type,
                                  exercise_type=exercise_type,
                                  fitness_goal=fitness_goal,
                                  qr_code = qr_code,
                              )
                              user_profile.save()
                              user.save()
                       
                              auth_user = authenticate(request, username=user_name, password=password)
                              if auth_user is not None:
                                  login(request, auth_user)
                                  request.session['full_name'] = full_name
                                  request.session['userphone'] = user_name
                                  request.session['gym_house'] = gym_house
                                  return redirect('home')
                              else:
                                  messages.error(request, "Invalid password for imported user.")
                                  break
                          else:
                             messages.error(request, "Invalid password, please try to remember or reset it.")

                          
            else:
                messages.error(request, "Username or Phone number doesn't exist. Please sign up.")

        except Exception as e:
            messages.error(request, f"An error occurred: {str(e)}")

    return render(request, 'Login.html')


def user_logout(request):
  logout(request)
  response = redirect('login')  # Redirect to the login page or another page
  response['Cache-Control'] = 'no-cache, no-store, must-revalidate'
  response['Pragma'] = 'no-cache'
  response['Expires'] = '0'
  return response


def forget_password(request):
  
  if request.method == 'POST':
    phone_number = request.POST.get('phone_number')
    
    try:
      user = User.objects.get(userprofile__phone_number = phone_number)
      username = user.username
      if user:
        request.session['phone_number'] = phone_number
        request.session['username'] = username
        
        result = send_verification_code()
      
        if result['status'] == 'success':
          return redirect(result['redirect'])
        elif result['status'] == 'error':
          print('API error:', result['message'])
        else:
          print(f"HTTP error ... code: {result['code']}, msg: {result['message']}")

        return redirect('password_reset')
      else:
        return redirect('login')
    except ObjectDoesNotExist:
      messages.error(request, 'No profile found for this phone number.')
      return redirect('login')
      

  return render(request, 'Forget-password.html')


def password_reset(request):
  phone_number = request.session.get('phone_number')
  username = request.session.get('username')
  user = User.objects.get(username = username)
  if username:
    profile = UserProfile.objects.get(user = user)
    full_name = profile.full_name

    if request.method == 'POST': 
      #handling the entered_otp, password and new_password
             
      entered_otp = request.POST.get('otp').strip()
      
      session = requests.Session()
      base_url = 'https://api.afromessage.com/api/verify'
      token = 'eyJhbGciOiJIUzI1NiJ9.eyJpZGVudGlmaWVyIjoidkc4ZUZacm55eW1xbDVMQ3VSVEZwRmlRZUxhNmhxVnoiLCJleHAiOjE5MTAwMTI4NTUsImlhdCI6MTc1MjI0NjQ1NSwianRpIjoiN2ZkZmUyZWMtMGUwYS00YTNiLWIyNjgtYTYzZDk1NmE1YWU4In0.cx3izFES9LXG_LfSOf0jCa0USP9zl1iacbrAL29Sr44'
      headers = {'Authorization': 'Bearer ' + token}
      to = '+251963719303'
      code = entered_otp

      url = '%s?to=%s&code=%s' % (base_url, to, code)
      result = session.get(url, headers=headers)
      
      new_password = request.POST.get('password')
      con_password = request.POST.get('con_password')
      
      if new_password == con_password and result.status_code == 200:
        
        json = result.json()
        if json['acknowledge'] == 'success':

          user = User.objects.get(username = username)
          user.set_password(new_password)
          user.save()
          messages.success(request, 'Your changed your password succesfully, now you can login using your new password.')
      else:
        messages.error(request, 'The new password and confirm password do not match')
        result.status_code = 300
        
      if result.status_code == 200:
          json = result.json()
          if json['acknowledge'] == 'success':
              messages.success(request, 'Your changed your password succesfully, now you can login using your new password.')
              return redirect('login')
          else:
              messages.error(request, 'The otp you entered is incorrect, try again')

      else:
          print('HTTP error ... code: %d, msg: %s' % (result.status_code, result.content))
     
    return render( request, 'Password-reset.html', {'phone_number': phone_number, 'full_name': full_name})

  else: 
     messages.error(request, 'Please try again later.')
     return redirect('login')
  

  # This is a function for trying, debugging, and implementing new features
import qrcode
import base64
import json
from io import BytesIO

def trial_stuffs(request):
   
   gymers = get_gymers_collection()
   result = []

   collections = gymers.find({})
   for collection in  collections:
      gym_house_name = collection.get('name')
      print(gym_house_name)

      if gym_house_name == 'Oxygen':
         gymers.update_many  ( 
            {"name": "Oxygen"},
            { "$unset": {"name": ''}}
         )
  

      for user in collection.get('users', []):
         print(user.get('userName'))   

      #Handle the qr code

      user_data = {
          "name": "dagmawi_t",
          "email": 18,
          "phone_number": "+251912345678"
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

     

   

   return render(request, 'trial.html', {'qr_code':  img_base64})