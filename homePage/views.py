from django.shortcuts import render, redirect
from Gymnify.mongo_utils import get_gymers_collection
from django.contrib import messages
from datetime import datetime
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User 
from userMember.models import UserProfile 
from allauth.socialaccount.models import SocialAccount
import random
import json
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from dateutil.relativedelta import relativedelta
from django.db.models import Q


@login_required

def home_page(request):
  gymers_collection = get_gymers_collection()
  userphone = request.session.get('userphone')
  request.session['username'] = userphone
  user = request.user
  context = {
        'userphone': userphone,
        'first_name': request.session.get('first_name', ''),
        'last_name' : '',
        }
  
  if userphone and (User.objects.filter(username = userphone).exists() or User.objects.filter(userprofile__phone_number = userphone)):
      profile= UserProfile.objects.get(user = user)
      gym_house_email = gymers_collection.find_one(
        {'users.userName': profile.user.username},
        {'email': 1}
      ).get('email', None)
      
      gym_house_phone = gymers_collection.find_one (
        {'users.userName': profile.user.username},
        {'phoneNumber': 1}
      ).get('phoneNumber', None)
      
      gym_house_name = gymers_collection.find_one (
        {'users.userName': profile.user.username},
        {'name': 1}
      ).get('name', None)
      
      result = gymers_collection.find_one(
    {'users.userName': profile.user.username},
    {'users.$': 1}  )
      if result:
        #registration date calculation
        
        date_obj = datetime.strptime(result['users'][0].get('registeredDate', None), '%d, %m, %Y'  )
        registeredDate = date_obj.strftime('%B %d %Y G.C')
        current_time = datetime.now()
        days_of_registration = (current_time - date_obj).days
        
        #membership detail handling
        membership_detail = result['users'][0].get('membershipDetail')
        if membership_detail:
          detail_list = list(membership_detail)
          for item in detail_list:
            plan_name = item['planName']
            package_length = item['packageLength']
            price = item['price']
            
            #calculating the next payment date 
            import re
            package_number = re.search(r'\d+', package_length).group() 
            payment_obj = date_obj + relativedelta(months = int(package_number))
            next_payment_date = payment_obj.strftime('%B %d %Y')
            obj_payment_date = datetime.strptime(next_payment_date, '%B %d %Y')
            days_left = (obj_payment_date - datetime.now()).days
            paymentDate = obj_payment_date.strftime('%d, %m, %Y')
            gymers_collection.update_one ( 
                  {'users.userName': profile.user.username},
                  {'$set': 
                    {
                      'users.$.paymentDate': paymentDate
                    }
                    })
          
                  
        else: 
          messages.error(request, f"You haven't purchased a membership package from {gym_house_name} Gym yet. Please select a price plan to continue")
          plan_name, package_length, price, next_payment_date, days_left = '', '', '', '', ''
          return redirect('pricingplan')
      if profile:
        phone_number = profile.phone_number
        phone_verified = profile.phone_verified
        if phone_number and phone_verified:
          context['first_name'] = profile.first_name.capitalize()
          context['last_name'] = profile.last_name.capitalize()
          first_name = context['first_name']
          last_name = context['last_name']
          request.session['first_name'] = first_name
          request.session['last_name'] = last_name
  
          context = {
                  'first_name': request.session['first_name'],
                  'last_name': request.session['last_name'],
                  'profile_photo': profile.profile_photo,
                  'gym_house_email': gym_house_email,
                  'gym_house_phone': gym_house_phone,
                  'gym_house_name': gym_house_name,
                  'registeredDate': registeredDate,
                  'days_of_registration': days_of_registration,
                  'plan_name': plan_name,
                  'package_length': package_length,
                  'price': price,
                  'next_payment_date': next_payment_date,
                  'days_left': days_left
              }
          

        
      
          messages.success(request, f'You are signed successfully as {userphone} ')
          
          
        else:
          username = request.session.get('username')
          messages.error(request,'Please insert and verify your phone number, for further validation')
          return redirect('insertion')
        
        
  #social account handling
        
  elif SocialAccount.objects.filter(user=user).exists():
    user_email = request.user.email
    user_username = request.user.username
    request.session['username'] = user_username
    profile = UserProfile.objects.filter(email = user_email).first()
    
    
    if profile:
      phone_number = profile.phone_number
      phone_verified = profile.phone_verified
      request.session['user_username'] = profile.user.username
      if phone_number and phone_verified:
          first_name = profile.first_name
          last_name = profile.last_name
          profile_photo = profile.profile_photo
        
          request.session['first_name'] = first_name
          request.session['last_name'] = last_name
          
          gym_house_email = gymers_collection.find_one(
                  {'users.userName': profile.user.username},
                  {'email': 1}
                ).get('email', None)
                
          gym_house_phone = gymers_collection.find_one (
                  {'users.userName': profile.user.username},
                  {'phoneNumber': 1}
                ).get('phoneNumber', None)
                
          gym_house_name = gymers_collection.find_one (
                  {'users.userName': profile.user.username},
                  {'name': 1}
                ).get('name', None)
          result = gymers_collection.find_one(
                  {'users.userName': profile.user.username},
                  {'users.$': 1}  )
          
          if result:
            #registration date calculation
            
            date_obj = datetime.strptime(result['users'][0].get('registeredDate', None), '%Y, %m, %d'  )
            registeredDate = date_obj.strftime('%B %d %Y G.C')
            current_time = datetime.now()
            days_of_registration = (current_time - date_obj).days
            
            #membership detail handling
            
            membership_detail = result['users'][0].get('membershipDetail')
            if membership_detail:
              detail_list = list(membership_detail)
              for item in detail_list:
                plan_name = item['planName']
                package_length = item['packageLength']
                price = item['price']
                
                #calculating the next payment date 
                import re
                package_number = re.search(r'\d+', package_length).group() 
                payment_obj = date_obj + relativedelta(months = int(package_number))
                next_payment_date = payment_obj.strftime('%B %d %Y')
                obj_payment_date = datetime.strptime(next_payment_date, '%B %d %Y')
                days_left = (obj_payment_date - datetime.now()).days
                paymentDate = obj_payment_date.strftime('%d, %m, %Y')
                gymers_collection.update_one ( 
                    {'users.userName': profile.user.username},
                    {'$set': 
                      {
                        'users.$.paymentDate': paymentDate
                      }
                      })
          
            else: 
              messages.error(request, f"You haven't purchased a membership package from {gym_house_name} Gym yet. Please select a price plan to continue")
              plan_name, package_length, price, next_payment_date, days_left = '', '', '', '', ''
              return redirect('pricingplan')
          
              
          
          
          context = {
            'first_name': first_name,
            'last_name': last_name,
            'profile_photo': profile_photo,
            'gym_house_email': gym_house_email,
            'gym_house_phone': gym_house_phone,
            'gym_house_name': gym_house_name,
            'registeredDate': registeredDate,
            'days_of_registration': days_of_registration,
            'plan_name': plan_name,
            'package_length': package_length,
            'price': price,
            'next_payment_date': next_payment_date,
            'days_left': days_left
          }
              
      else:
          username = request.session.get('username')
          messages.error(request,'Please insert and verify your phone number, for further validation')
          return redirect('insertion')
    
    else:
      
      first_nameGoggle = request.user.first_name
      last_nameGoggle = request.user.last_name
      
     #Generating a random username for the user
     
      unique_number = random.randint(100, 999)
      pre_username = f"{first_nameGoggle[:2].lower()}{last_nameGoggle[:2].lower()}"
      username = f'{pre_username}{unique_number}'
      
      myuser = User.objects.create(username = username)
      user_profile = UserProfile(user = myuser, first_name = first_nameGoggle, last_name = last_nameGoggle, email = request.user.email)
      myuser.save()
      user_profile.save()
      
      context = {
        'first_nameGoggle': first_nameGoggle,
        'last_nameGoggle': last_nameGoggle
        }
      messages.error(request,'Please insert your phone number, for further validation')

      request.session['username'] = username
    

      return redirect('insertion')
    
    
    return render(request, 'homePage.html', context)
         
  else: 
    messages.error(request, "You have not signed up successfully yet. ")
    return redirect('login')  
  
  

  return render(request, 'homePage.html', context)
 



from django.shortcuts import render
from pymongo import MongoClient


from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def profilePage(request):
    
  userGoggle = request.user.email
  user = request.user
  gymers_collection = get_gymers_collection()

  if user or userGoggle:
    
        profile = UserProfile.objects.filter(Q(user=user) | Q(email = userGoggle)).first()
        if profile:
            username = profile.user.username
            first_name = profile.first_name.capitalize()
            last_name = profile.last_name.capitalize()
            profile_photo = profile.profile_photo
            email = profile.email
            age = profile.age
            weight = profile.weight
            height= profile.height
            exercise_type = profile.exercise_type
            gender = profile.gender
            exercise_day = profile.exercise_day
            blood_type = profile.blood_type
            health_status= profile.health_status
            exercise_time_per_day = profile.exercise_time_per_day
            fitness_goal = profile.fitness_goal
            notificationTime = profile.notificationTime
            enteringTime = profile.enteringTime
            totalTimeSpendOnGym = profile.totalTimeSpendOnGym
            activityLevel = profile.activityLevel
            
                
            if request.method == 'POST' and request.FILES.get('profile_photo'):
               profile = UserProfile.objects.filter(Q(user=user) | Q(email = userGoggle)).first()
               if request.FILES.get('profile_photo'):
                  profile_photo = request.FILES.get('profile_photo')
                  profile.profile_photo = profile_photo
                  profile.save()
                  redirect('profilepage')
                  
            if request.method == 'POST' and not request.FILES.get('profile_photo'):
              
                  email = request.POST.get('email')
                  age = request.POST.get('age')
                  weight = request.POST.get('weight')
                  height = request.POST.get('height')
                  gender = request.POST.get('gender', 'M')
                  exercise_day = request.POST.get('exercise_day')
                  health_status = request.POST.get('health_status')
                  exercise_type = request.POST.get('exercise_type')
                  blood_type = request.POST.get('blood_type')
                  exercise_time_per_day = request.POST.get('exercise_time_per_day')
                  fitness_goal= request.POST.get('fitness_goal')
                  notificationTime = request.POST.get('notificationTime')
                  enteringTime = request.POST.get('enteringTime')
                  totalTimeSpendOnGym = request.POST.get('totalTimeSpendOnGym')
                  activityLevel = request.POST.get('activityLevel')
                  print(activityLevel)
                  
                  profile = UserProfile.objects.filter(Q(user=user) | Q(email = userGoggle)).first()
                  
                  profile.email = email
                  profile.age = age
                  profile.weight = weight
                  profile.height = height
                  profile.gender = gender
                  profile.exercise_day = exercise_day
                  profile.health_status = health_status
                  profile.exercise_type = exercise_type
                  profile.blood_type = blood_type
                  profile.fitness_goal = fitness_goal
                  profile.exercise_time_per_day = exercise_time_per_day
                  profile.notificationTime = notificationTime
                  profile.enteringTime = enteringTime
                  profile.totalTimeSpendOnGym = totalTimeSpendOnGym
                  profile.activityLevel = activityLevel
                  profile.save()
                  
                  #mongoDB insertion using $set 
                  
                  gymers_collection.update_one(
                  {'users.userName': username},
                  {
                    '$set':  {
                      
                      "users.$.email": email,
                      "users.$.age": age,
                      "users.$.weight": weight,
                      "users.$.height": height,
                      "users.$.sex": gender,
                      "users.$.exerciseTimePerDay": exercise_time_per_day,
                      "users.$.healthStatus": health_status,
                      "users.$.fitnessGoal": fitness_goal,
                      "users.$.bloodType": blood_type,
                      "users.$.exerciseType": exercise_type,
                      "users.$.notificationTime": notificationTime,
                      "users.$.enteringTime": enteringTime,
                      "users.$.totalTimeSpendOnGym": totalTimeSpendOnGym,
                      "users.$.activityLevel": activityLevel
                    }
                  }
                )

  if not user: 
   messages.error(request, f'Please login first to access the profile page')
   return redirect('login')
 
  context = {
    'username': username,
    'first_name': first_name,
    'last_name': last_name,
    'profile_photo': profile_photo,
    'email': email,
    'age': age,
    'weight': weight,
    'height': height,
    'exercise_type': exercise_type,
    'gender': gender,
    'exercise_day': exercise_day,
    'blood_type': blood_type,
    'health_status': profile.health_status,
    'exercise_time_per_day': exercise_time_per_day,
    'fitness_goal': fitness_goal,
    'notificationTime': notificationTime,
    'enteringTime': enteringTime,
    'totalTimeSpendOnGym': totalTimeSpendOnGym,
    "activityLevel": activityLevel
      
  } 
 
  return render(request, 'profilePage.html', context)


@csrf_exempt

def pricingPlan(request):
  user = request.user
  gymers_collection = get_gymers_collection()
  username = request.session.get('user_username', '')
  request.session['username'] = username

  if username:
    user_account = User.objects.get(username = username)
  else:
    user_account = None
  if user.is_authenticated:
    
    #checking whether the user is username or request.user
    
    profile = UserProfile.objects.get(Q(user = user) | Q(user = user_account))
    username = profile.user.username
    gym_house_name = gymers_collection.find_one(
    {'users.userName': username},
    {'name': 1}).get('name', None)
  
    #rendering gym plans
    
    gym_data = gymers_collection.find_one(
      {'users.userName': username},
      {}
      )
    
    member_ship = gym_data.get('memberShip', {})
    
    has_any_plan = any('1' in details and details['1'] != "" for details in member_ship.values())
    
    context = {
      'gym_house_name': gym_house_name,
      'member_ship': member_ship,
      'has_any_plan': has_any_plan
    }
  
    return render(request, 'pricingPlan.html', context )

  else:
    return redirect('register')
  
def submitPricingPlan(request):
  
    gymers_collection = get_gymers_collection()
    user = request.user
    username = request.session.get('username')
    
    if username:
      user_account = User.objects.get(username = username)
    else:
      user_account = None
    profile = UserProfile.objects.get(Q(user = user) | Q(user = user_account))
  
    if request.method == 'POST':
    
      data = json.loads(request.body)
      plan_name = data.get('plan_name', 'N/A')
      selected_duration = f"{data.get('selected_duration', 'N/A')} month"
      price = data.get('price', 'N/A')
    
      membership_level = {
        'planName': plan_name,
        'packageLength': selected_duration,
        'price': price
      }
      
      gymers_collection.update_one(
        {'users.userName': profile.user.username},
        {'$push': {'users.$.membershipDetail': membership_level}}
      )
      
      return JsonResponse({
                    'status': 'success',
                    'message': 'Plan added successfully to user',
                    'data': membership_level,
                    'redirect_url': '/home'
                })
      

      
    