# views.py placeholder
from django.shortcuts import render, redirect
from .forms import ExerciseForm
from django.contrib import messages

def add_exercise(request):
    if request.method == 'POST':
        form = ExerciseForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'The Exercise is added succesfully')
            return redirect('add_exercise')
            
    else:
        form = ExerciseForm()
    return render(request, 'exercises/exercise_form.html', {'form': form})


from .models import Exercise

def list_exercises(request):
    exercises = Exercise.objects.all()
    return render(request, 'exercises/exercise_list.html', {'exercises': exercises})


from django.shortcuts import get_object_or_404

def edit_exercise(request, exercise_id):
    exercise = get_object_or_404(Exercise, id=exercise_id)
    if request.method == 'POST':
        form = ExerciseForm(request.POST, instance=exercise)
        if form.is_valid():
            form.save()
            messages.success(request, 'The Exercise is edited successfully')

            return redirect('list_exercises')

    else:
        form = ExerciseForm(instance=exercise)
    return render(request, 'exercises/exercise_form.html', {'form': form})


def delete_exercise(request, exercise_id):
    exercise = get_object_or_404(Exercise, id=exercise_id)
    if request.method == 'POST':
        exercise.delete()
        messages.success(request, 'The Exercise is deleted succesfully')

        return redirect('list_exercises')

    return render(request, 'exercises/delete_confirm.html', {'exercise': exercise})

from .models import Alternative

def alternative_list(request):
    alternatives = Alternative.objects.all()
    return render(request, 'alternatives/list.html', {'alternatives': alternatives})

def alternative_detail(request, pk):
    alternative = get_object_or_404(Alternative, pk=pk)
    return render(request, 'alternatives/detail.html', {'alternative': alternative})
