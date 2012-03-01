from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect , HttpResponse
from django.template.loader import get_template
from django.template import Context

import models
import AutoArranger


def index(request):
    
    t = get_template('defendcalendar.html')
    projects_list = list(models.Project.objects.all())
    c = Context(dict(events = projects_list))
    html = t.render(c)

    return HttpResponse(html)
    

def arrange(request , days , rules):
    a = AutoArranger.AutoArranger()
    a.arrange_by_bussy_days(days)
    
    return HttpResponseRedirect(reverse('projectbook.apps.project_calendar.admin_views.index'))
