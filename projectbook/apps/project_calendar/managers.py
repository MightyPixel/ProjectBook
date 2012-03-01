from django.db.models import Manager

import models

class EventManager(Manager):
    def get_projects_for_date(self , date , spec):
        return len(models.Event.objects.filter(spec = spec).filter(project__commission__date = date))
        
  
