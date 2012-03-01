from django import forms
from django.contrib.admin import widgets

class ArrangeForm(forms.Form):
    mentor = forms.BooleanField()
    reviewer = forms.BooleanField()
    start_date = forms.DateTimeField(widget=widgets.AdminDateWidget())
    end_date = forms.DateTimeField(widget=widgets.AdminDateWidget())
