import datetime

from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.template.loader import get_template
from django.http import HttpResponse , HttpResponseRedirect
from django.template import Context
from django.shortcuts import render_to_response
from django.contrib.admin.views.decorators import staff_member_required

import models
import forms

from projectbook.apps.project_arrange.models import Project
from projectbook.apps.project_arrange.models import Commission

def index(request):

    if request.method == 'POST': # If the form has been submitted...
        form = forms.ArrangeForm(request.POST) # A form bound to the POST data
        if form.is_valid(): # All validation rules pass
            # Process the data in form.cleaned_data
            # ...
            return HttpResponseRedirect('/admin/arrange/') # Redirect after POST
    else:
        form = forms.ArrangeForm()

    sw_event_list = models.Event.objects.filter(spec__spec_type = 'sw')
    hw_event_list = models.Event.objects.filter(spec__spec_type = 'hw')
    nw_event_list = models.Event.objects.filter(spec__spec_type = 'nw')

    return render_to_response(
        'defendcalendar.html',
        {'sw_events' : sw_event_list , 'hw_events' : hw_event_list , 'nw_events' : nw_event_list },
        RequestContext(request, {'form' : form}),
    )
index = staff_member_required(index)


def create_events(request):
    t = get_template('defendcalendar.html')
    
    models.Event.objects.all().delete()

    projects_list = Project.projects.get_this_year_projects()
    
    print projects_list
    
    for project in projects_list:
        print project.commission
        if project.commission:
            event = models.Event()
            event.project = project
            event.save()
            event.title = project.title
            event.day_index = Commission.commissions.get_projects_count(project.commission)
            event.start = datetime.datetime(year = event.project.year ,
                                            month = project.commission.date.month,
                                            day = project.commission.date.day,
                                            hour = models.Event.events.get_projects_for_date(project.commission.date,
                                                project.commission.specialty) + 8)
            event.end = datetime.datetime(year = project.year ,
                                            month = project.commission.date.month,
                                            day = project.commission.date.day,
                                            hour = models.Event.events.get_projects_for_date(project.commission.date,
                                                project.commission.specialty) + 9)
            event.spec = project.commission.specialty
            if project.commission.specialty.room != None:
                event.room = project.commission.specialty.room
            event.save()

    return HttpResponseRedirect(reverse('projectbook.apps.project_calendar.admin_views.index'))

create_events = staff_member_required(create_events)
