from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from userMember.models import UserProfile 
from django.core.cache import cache
from mealplanner.utils import calculate_targets
from userMember.models import UserFastingLog
from datetime import date
from .utils import meal_plan
from django.contrib import messages
from django.contrib.auth.models import User



@login_required
def nutrition_planner(request):
    profile = UserProfile.objects.filter(user=request.user).first()
    today = date.today()
    userfastinglog = UserFastingLog.objects.filter(user=request.user, date=today).first()
    if not userfastinglog:
        messages.error(request, 'Please tell us whether you are fasting or not')
        return redirect('additional_info')
        
    cache_key = f'nutrition_targets_user_{request.user.id}'
    cached_targets = cache.get(cache_key)

    if cached_targets:
        targets = cached_targets
    else:
        targets = calculate_targets(profile)
        cache.set(cache_key, targets, timeout=86400)

    plan_data = meal_plan(profile, userfastinglog)

    context = {
        "profile": profile,
        "targets": targets,
        "plan": plan_data.get("plan", {})
    }

    return render(request, "Nutrition_planner.html", context)


@login_required

def addition_info(request):
    user = request.user
    today = date.today()
    profile = UserProfile.objects.filter(user=user).first()
    userfastinglog = UserFastingLog.objects.filter(user=user).first()

    if request.method == "POST":
        if userfastinglog:
            userfastinglog.user = request.user
            userfastinglog.is_fasting = request.POST.get('is_fasting', 'no').lower() == 'yes'
            userfastinglog.save()
            return redirect('nutrition_planner')
        else:
            userfastinglog = UserFastingLog(user=user, is_fasting = request.POST.get('is_fasting', 'no').lower() == 'yes', date = today )
            userfastinglog.save()
    return render(request, "Addition_info.html", {"user": user, "profile": profile,})