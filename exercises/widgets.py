from django import forms
from django.utils.html import format_html
from django.utils.safestring import mark_safe

class AlternativeCheckboxRenderer(forms.CheckboxSelectMultiple):
    template_name = 'widgets/custom_checkbox_option.html'
