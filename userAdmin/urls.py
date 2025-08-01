from django.contrib import admin
from django.urls import path, include
from userAdmin import views
urlpatterns = [
    path('user-admin-dashboard', views.user_admin_dashboard, name = 'user_admin_dashboard'),
    path('user-admin-income', views.user_admin_income, name = 'user_admin_income'),
    path('user-admin-data-entry', views.user_admin_data_entry, name = 'data_entry'),
    path('admin/', admin.site.urls),
    path('toggle-status/', views.toggle_status, name = 'toggle_status'),
    path('message', views.message, name = 'message'),
    path('delete-notification', views.delete_notification, name = "delete_notification"),
]
