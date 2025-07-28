from django.contrib import admin
from django.urls import path, include
from userMember import views
from rest_framework_simplejwt.views import TokenObtainPairView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('homePage.urls')),
    path('', include('validation.urls')),
    path('', include('userMember.urls')),
    path('', include('userAdmin.urls')),
    path('', include('exercises.urls')),
    path('accounts/', include('allauth.urls')), 
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
   
]
