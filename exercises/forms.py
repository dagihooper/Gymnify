from django import forms
from .models import Exercise, Alternative

class ExerciseForm(forms.ModelForm):
    alternatives = forms.ModelMultipleChoiceField(
        queryset=Alternative.objects.all(),
        required=False,
        widget=forms.CheckboxSelectMultiple
    )

    class Meta:
        model = Exercise
        fields = '__all__'