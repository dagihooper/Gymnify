from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('home/', views.home_page, name='home'),
    path('pricingplan', views.pricingPlan, name = 'pricingplan'),
    path('profilepage/', views.profilePage, name = 'profilepage'),
    path('checking_profile/', views.checkingProfile, name = 'checking_profile'),
    path('home/meal/', include('mealplanner.urls')),
    path('submitpricingplan', views.submitPricingPlan, name = 'submitpricingplan')
]  + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

