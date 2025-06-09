from django.contrib import admin
from django.urls import path, include
from userMember import views
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('homePage.urls')),
    path('', include('validation.urls')),
    path('', include('userMember.urls')),
    path('', include('userAdmin.urls')),
    path('accounts/', include('allauth.urls')), 
    


]
