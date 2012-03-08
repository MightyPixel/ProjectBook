from django import forms
from django.contrib.admin import widgets

class ArrangeForm(forms.Form):
    mentor = forms.BooleanField()
    reviewer = forms.BooleanField()
    start_date = forms.DateTimeField(widget=widgets.AdminDateWidget())
    end_date = forms.DateTimeField(widget=widgets.AdminDateWidget())
    start_hour = forms.TimeField(widget=widgets.AdminTimeWidget())
    half_hour = forms.TimeField(widget=widgets.AdminTimeWidget())
    end_hour = forms.TimeField(widget=widgets.AdminTimeWidget())
    commission_size = forms.IntegerField()
    max_projects = forms.IntegerField()
    
