from django.shortcuts import render, redirect
from Gymnify.mongo_utils import get_gymers_collection
from datetime import datetime
from django.views.decorators.csrf import csrf_exempt
import json
from django.http import JsonResponse
from bson import ObjectId
from dateutil.relativedelta import relativedelta


def user_admin_dashboard(request):
  
    gymers_collection = get_gymers_collection()
    gymers = list(gymers_collection.find())
    total_users = 0
    notification_data = []

    #iterating 
    
    for gymer in gymers:
        gymer['gymer_id'] = str(gymer['_id'])  #
          
         #for time line
        registered_date = datetime.strptime(gymer.get('registeredDate')
, "%d, %m, %Y")
        current_date = datetime.now().date()
        delta = current_date - registered_date.date()
        expiry_date = registered_date + relativedelta(months=1)
        formatted_expiry_date = expiry_date.strftime('%B, %d, %Y')
        days_left = (expiry_date.date() - current_date).days
        print(days_left)
        gymer['timeline'] = delta.days
        
        #for service type
                
        if str(gymer.get('pricePlan')).strip() == '5316':
          gymer['service_type'] = 'Introductory'
        elif str(gymer.get('pricePlan')).strip() == '11000':
          gymer['service_type'] = 'Standard'
        else :
          gymer['service_type'] = 'Unknown'
          
          
          #handle the notification stuffs
        
        notifications = list(gymer['notificationAdmin'])

        for notification in notifications:
          
          if '_id' not in notification: 
              notification['_id'] = ObjectId()  
              print(gymer['notificationAdmin'])
              
              
             
          gymers_collection.update_one ( {
               'name': gymer['name']},
               {
                 "$set":  {
                   "notificationAdmin": gymer['notificationAdmin']
                 }
               }
             )
          
          if notification['type'] == 'Package Expiry':
             notification_data.append({
                "type": notification['type'],
                "id": notification['_id'],
                "company": gymer['name'],
                "package": gymer['service_type'],
                "date": notification['date']
            })
             
          
             
             
           #for handle the sending notification to notficationAdmin
           
          if days_left in (90, 75, 50, 35, 20, 5, 3):

            print('days left found in ')
            print(days_left)
                
            existing_notification = gymers_collection.find_one({
                        'name': gymer['name'],
                        'notificationAdmin': {
                            '$elemMatch': {
                                'type': 'Package Expiry',
                                'days_left': days_left
                            }
                        }
                    })

            if not existing_notification:
                gymers_collection.update_one(
                    {'name': gymer['name']},
                    {'$push': {
                        'notificationAdmin': {
                            'type': 'Package Expiry',
                            'date': datetime.now(),
                            'days_left': days_left
                        }
                    }}
                )
             

      
        #for payment status 
        
        if gymer.get('payDone'):
          gymer['payment_status'] = 'Active'
        else :
          gymer['payment_status'] = 'Inactive'
          
        #for total customers, total members and active customers
        user_array  = gymer.get('users')
        total_users += len(user_array) 
        
        
       
          
          
        
        
        
        
         #context
         
        print('here is the notification data of the page ')
             
        context = {
          'gymers': gymers,
          'total_customers': gymers_collection.count_documents({}),
          'total_active_users': gymers_collection.count_documents({'payDone': True}),
          'total_users':  total_users,
          'notifications': notification_data,
          'expiry_date': formatted_expiry_date,
          'days_left': days_left,
          
        }


    return render(request, 'user-admin-dashboard.html', context)


def user_admin_income(request):
  
  gymers_collection = get_gymers_collection()
  gymers = list(gymers_collection.find())
  

  for gymer in gymers:
    gymer['_id'] = str(gymer['_id'])  
    
    if gymer.get('payDone'):
      gymer['payment_status'] = 'Active' 
      payments_list = gymer.get('paymentsList', [])
      if payments_list:
          for payment in payments_list:
            gymer['date_of_payment'] = payment.get('date_of_payment', 'N/A')
            gymer['price'] = str(gymer.get('pricePlan')).strip()
            total_balance += gymer.get('pricePlan', 0)
            

            #handle the datetime logic
            
            current_date = datetime.now()
            current_month = current_date.month
            current_year = current_date.year
            payment_date = datetime.strptime(gymer['date_of_payment'], '%d, %m, %Y')
            gymer['date'] = datetime.strptime(gymer['date_of_payment'], '%B, %m, %d')
            if payment_date.month == current_month and payment_date.year == current_year:
              total_montly_income += gymer.get('pricePlan', 0)
      
      else: 
         payments_list,total_balance,total_montly_income = '', 0, 0
 

      

   
         #for service type
             
      if str(gymer.get('pricePlan')).strip() == '5316':
        gymer['service_type'] = 'Introductory'
      elif str(gymer.get('pricePlan')).strip() == '11000':
        gymer['service_type'] = 'Standard'
      else :
        gymer['service_type'] = 'Unknown'
              
    else:
       payments_list,total_balance,total_montly_income = '', 0, 0
       
  context = {
      'gymers': gymers,
      'payments': payments_list,
      'total_active_users': gymers_collection.count_documents({'payDone': True}),
      'total_balance': total_balance,
      'total_monthly_income' : total_montly_income,
    }
  
  print(context['payments'])
    
    
        
    
  return render(request, 'user-admin-income.html', context )


@csrf_exempt
def toggle_status(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            gymer_id = ObjectId(data.get("gymer_id"))
            gymers_collection = get_gymers_collection()
            # Find the gym member
            gymer = gymers_collection.find_one({"_id": gymer_id})
            if not gymer:
                return JsonResponse({"success": False, "error": "Gymer not found"})

            # Toggle payDone status
            new_status = not gymer.get("payDone", False)
            gymers_collection.update_one({"_id": gymer_id}, {"$set": {"payDone": new_status}})

            return JsonResponse({"success": True, "new_status": new_status})
        except Exception as e:
            return JsonResponse({"success": False, "error": str(e)})
    return JsonResponse({"success": False, "error": "Invalid request method"})
  
  
  
def message(request):
  gymers_collection = get_gymers_collection()
  gymers = list(gymers_collection.find())
  
  
  if request.method == "POST":
    gym_house = request.POST.get('gym_house')
    message = request.POST.get('message')
    
    gymers_collection.update_one (
      {'name': gym_house}, 
      {"$push": {
            'notificationOperator': message
          }
        
      }
    )
  return render(request, 'Message.html', {'gymers': gymers})


def delete_notification(request):
  
  gymers_collection = get_gymers_collection()
  
  if request.method == 'POST': 
    import json
    from django.http import JsonResponse
    from bson import ObjectId
    data = json.loads(request.body)
    notificationId = ObjectId(data.get('id'))
    company = data.get('company')
    
    print(notificationId)
    

    
    gymers_collection.update_one( {
      'name': company
    }, {
      "$pull": {
        "notificationAdmin": {
          "_id": notificationId
        }
        
      }
    })
    
    
    
    
    return JsonResponse({'status': 'success'})
  
  return redirect('user_admin_dashboard')

