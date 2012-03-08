import datetime

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
    

def arrange(request):
    a = AutoArranger.AutoArranger()

    day_list = []
    respect_reviewer = False
    respect_mentor = False

    try:
        post = request._get_post()
        start = post.__getitem__('start_date')
        end = post.__getitem__('end_date')

        if post.__getitem__('mentor') == "no":
            respect_mentor = False
        else:
            respect_mentor = True

        if post.__getitem__('reviewer') == "no":
            respect_reviewer = False
        else:
            respect_reviewer = True
    except:
        pass

    it = datetime.datetime(year = int(start.split('-')[0]) , month = int(start.split('-')[1]) , day = int(start.split('-')[2]))
    end = datetime.datetime(year = int(end.split('-')[0]) , month = int(end.split('-')[1]) , day = int(end.split('-')[2]))
    while it <= end:
        day_list.append(it)
        it += datetime.timedelta(days=1)
    
    a.arrange_by_bussy_days(day_list , respect_mentor , respect_reviewer)
    
    return HttpResponseRedirect(reverse('projectbook.apps.project_calendar.admin_views.index'))
    
