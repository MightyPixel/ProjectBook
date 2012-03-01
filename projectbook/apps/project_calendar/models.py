from django.db import models

import managers
from projectbook.apps.project_arrange.models import Project
from projectbook.apps.project_arrange.models import Specialty


class Event(models.Model):
    project = models.ForeignKey(Project , null = True)
    day_index = models.SmallIntegerField(null = True)
    title = models.CharField(max_length=127 , null = True)
    start = models.DateTimeField(null=True)
    end = models.DateTimeField(null=True)
    room = models.CharField(max_length = 5 , default='1')
    spec = models.ForeignKey(Specialty , null=True)
    
    events = managers.EventManager()
    objects = models.Manager()
