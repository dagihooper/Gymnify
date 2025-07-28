from django.shortcuts import render, redirect
from Gymnify.mongo_utils import get_gymers_collection , get_bills_collection

from datetime import datetime
from django.views.decorators.csrf import csrf_exempt
import json
import re
from django.http import JsonResponse
from bson import ObjectId
from dateutil.relativedelta import relativedelta


def user_admin_dashboard(request):
  
    gymers_collection = get_gymers_collection()
    bills_collection = get_bills_collection()
    gymers = list(gymers_collection.find())
    bills = list(bills_collection.find())
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
        
        notifications = list(gymer['adminNotifications'])
        

        if notifications:

          for notification in notifications:
            if '_id' not in notification: 
                notification['_id'] = ObjectId()  
                
                
              
            gymers_collection.update_one ( {
                'name': gymer['name']},
                {
                  "$set":  {
                    "adminNotifications": gymer['adminNotifications']
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
           
          if days_left in (90, 75, 50, 35, 20, 5, 3 , 2, 1):



                
            existing_notification = gymers_collection.find_one({
                        'name': gymer['name'],
                        'adminNotifications': {
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
                        'adminNotifications': {
                            'type': 'Package Expiry',
                            'date': datetime.now(),
                            'days_left': days_left
                        }
                    }}
                )
             
          elif days_left <= 0:
               
              print('days left found in ')
              print(days_left)
                
              existing_notification = gymers_collection.find_one({
                          'name': gymer['name'],
                          'adminNotifications': {
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
                          'adminNotifications': {
                              'type': 'Package Expiry',
                              'date': datetime.now(),
                              'days_left': days_left
                          }
                      }}
                  )

        else:
           #for handle the sending notification to notficationAdmin
           
          if days_left in (90, 75, 50, 35, 20, 5, 3 , 2, 1):

            print('days left found in ')
            print(days_left)
                
            existing_notification = gymers_collection.find_one({
                        'name': gymer['name'],
                        'adminNotifications': {
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
                        'adminNotifications': {
                            'type': 'Package Expiry',
                            'date': datetime.now(),
                            'days_left': days_left
                        }
                    }}
                )
             
          elif days_left <= 0:
               
              print('days left found in ')
              print(days_left)
                
              existing_notification = gymers_collection.find_one({
                          'name': gymer['name'],
                          'adminNotifications': {
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
                          'adminNotifications': {
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
         
             
        context = {
          'gymers': gymers,
          'total_customers': gymers_collection.count_documents({}),
          'total_active_users': gymers_collection.count_documents({'payDone': True}),
          'total_users':  total_users,
          'notifications': notification_data,
          'expiry_date': formatted_expiry_date,
          'days_left': days_left,
          
        }
     
    return render(request, 'User-admin-dashboard.html', context)


def user_admin_income(request):
  
  gymers_collection = get_gymers_collection()
  gymers = list(gymers_collection.find())
  bills_collection = get_bills_collection()
  bills = list(bills_collection.find())

  payments_list_coll = []
  gym_house_name_coll = []
  balance = 0
  montly_income = 0

  for bill in bills:
            
      if bill:
            gym_house_name = bill['gym_name']
            print(gym_house_name)
            price = int(bill['price_plan'])
            date_of_payment = bill['date_of_payment']
            payment_date = date_of_payment
            print(payment_date)

            print(date_of_payment)
            # package_type = bill['package_type']
            # file_image = bill['fileType']
            # file_name  = bill['fileName']

            current_date = datetime.now()
            current_month = current_date.month
            current_year = current_date.year
            bill['date'] = payment_date.strftime('%B, %m, %d')
            total_balance = balance + price


            if payment_date.month == current_month and payment_date.year == current_year:
               total_montly_income = montly_income + price
            
    
            else: 
               payments_list,balance,montly_income = '', 0, 0

             
            if str(bill.get('price_plan')).strip() == '5316':
              bill['service_type'] = 'Introductory'
            elif str(bill.get('price_plan')).strip() == '11000':
              bill['service_type'] = 'Standard'
            else :
              bill['service_type'] = 'Unknown'
    
      else: 
          payments_list,balance,montly_income = '', 0, 0
  
  # for gymer in gymers:
  #   gymer['_id'] = str(gymer['_id'])  
    
  #   if gymer.get('payDone'):
  #     gymer['payment_status'] = 'Active' 
  #     payments_list = gymer.get('paymentsList', [])
  #     if payments_list:
  #         for payment in payments_list:
  #           payments_list_coll.append(payment)
  #           # gymer['date_of_payment'] = payment.get('date_of_payment', 'N/A')
  #           gymer['price'] = str(gymer.get('pricePlan')).strip()
  #           total_balance = balance + gymer.get('pricePlan', 0)
            

  #           #handle the datetime logic
            
  #           current_date = datetime.now()
  #           current_month = current_date.month
  #           current_year = current_date.year
  #           payment_date = datetime.strptime(gymer['date_of_payment'], '%d, %m, %Y')
  #           gymer['date'] = datetime.strftime(payment_date, '%B, %m, %d')
  #           if payment_date.month == current_month and payment_date.year == current_year:
  #             total_montly_income = montly_income + gymer.get('pricePlan', 0)
            
      
  #     else: 
  #        payments_list,balance,montly_income = '', 0, 0
 

      

   
  #        #for service type
             
  #     if str(gymer.get('pricePlan')).strip() == '5316':
  #       gymer['service_type'] = 'Introductory'
  #     elif str(gymer.get('pricePlan')).strip() == '11000':
  #       gymer['service_type'] = 'Standard'
  #     else :
  #       gymer['service_type'] = 'Unknown'
              
  #   else:
  #      payments_list,total_balance,total_montly_income = '', 0, 0
       
  context = {
      'bills': bills,
      # 'payments': payments_list_coll,
      'total_active_users': gymers_collection.count_documents({'payDone': True}),
      'total_balance': total_balance,
      'total_monthly_income' : total_montly_income,
    }
  
    
    
        
    
  return render(request, 'User-admin-income.html', context )


def user_admin_data_entry(request):
   return render(request, 'Data_Entry.html')


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
        "adminNotifications": {
          "_id": notificationId
        }
        
      }
    })
    
    
    
    
    return JsonResponse({'status': 'success'})
  
  return redirect('user_admin_dashboard')

