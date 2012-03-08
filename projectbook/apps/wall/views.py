import datetime

from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect , HttpResponse
from django.template.loader import get_template
from django.template import Context

from projectbook.apps.project_arrange.models import Project
from projectbook.apps.project_arrange.models import Commission
from projectbook.apps.project_calendar.models import Event

def vote(request, post_id):
    return HttpResponse("You're voting on post %s." % post_id)
    

def calendar(request):
    t = get_template('calendar.html')

    sw_event_list = Event.objects.filter(spec__spec_type = 'sw')
    hw_event_list = Event.objects.filter(spec__spec_type = 'hw')
    nw_event_list = Event.objects.filter(spec__spec_type = 'nw')
    
    c = Context(dict(sw_events = sw_event_list , hw_events = hw_event_list , nw_events = nw_event_list ))
    html = t.render(c)

    return HttpResponse(html)

