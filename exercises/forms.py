from django import forms
from .models import Exercise, Alternative
from django.utils.html import format_html
from django.urls import reverse

class AlternativeCheckboxRenderer(forms.CheckboxSelectMultiple):
    def create_option(self, name, value, label, selected, index, subindex=None, attrs=None):
        # Use label from label_from_instance, already formatted as HTML
        return super().create_option(name, value, label, selected, index, subindex=subindex, attrs=attrs)


class ExerciseForm(forms.ModelForm):
    class Meta:
        model = Exercise
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['alternatives'] = forms.ModelMultipleChoiceField(
            queryset=Alternative.objects.all(),
            required=False,
            widget=AlternativeCheckboxRenderer(),
            label="Alternatives"
        )

        self.fields['alternatives'].label_from_instance = self.custom_label_from_instance

        # Styling
        for field_name, field in self.fields.items():
            if isinstance(field.widget, (forms.TextInput, forms.Textarea, forms.NumberInput, forms.Select)):
                field.widget.attrs.update({
                    'class': 'border border-gray-300 rounded-md p-2 w-full focus:outline-none'
                })
            elif isinstance(field.widget, forms.CheckboxSelectMultiple):
                field.widget.attrs.update({
                    'class': 'space-y-2'
                })

    def custom_label_from_instance(self, alt):
        url = reverse('alternative_detail', args=[alt.pk])
        return format_html(
            '<a href="{}" class="text-blue-600 text-blue-400">{}</a>',
            url,
            alt.name
        )
