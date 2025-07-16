# views.py placeholder
from django.shortcuts import render, redirect
from .forms import ExerciseForm

def add_exercise(request):
    if request.method == 'POST':
        form = ExerciseForm(request.POST)
        if form.is_valid():
            form.save()
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
            return redirect('list_exercises')
    else:
        form = ExerciseForm(instance=exercise)
    return render(request, 'exercises/exercise_form.html', {'form': form})


def delete_exercise(request, exercise_id):
    exercise = get_object_or_404(Exercise, id=exercise_id)
    if request.method == 'POST':
        exercise.delete()
        return redirect('list_exercises')
    return render(request, 'exercises/delete_confirm.html', {'exercise': exercise})
