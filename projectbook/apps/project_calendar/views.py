import datetime

from django.shortcuts import render_to_response
from django.http import HttpResponse , HttpResponseRedirect
from django.template.loader import get_template
from django.template import Context

import models

from projectbook.apps.project_arrange.models import Project
from projectbook.apps.project_arrange.models import Commission

def index(request):
    t = get_template('defendcalendar.html')

    sw_event_list = models.Event.objects.filter(spec__spec_type = 'sw')
    hw_event_list = models.Event.objects.filter(spec__spec_type = 'hw')
    nw_event_list = models.Event.objects.filter(spec__spec_type = 'nw')
    
    c = Context(dict(sw_events = sw_event_list , hw_events = hw_event_list , nw_events = nw_event_list ))
    html = t.render(c)

    return HttpResponse(html)


