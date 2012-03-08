from django.contrib.admin import widgets
from django import forms

class ArrangeForm(forms.Form):
    mentor = forms.BooleanField()
    reviewer = forms.BooleanField()
    start_date = forms.DateTimeField(widget=widgets.AdminDateWidget())
    end_date = forms.DateTimeField(widget=widgets.AdminDateWidget())
    commission_size = forms.IntegerField()
    max_projects = forms.IntegerField()
    
