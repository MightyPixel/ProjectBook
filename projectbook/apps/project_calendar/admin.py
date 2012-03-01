from django.contrib import admin

import models
from projectbook.apps.project_arrange.admin import ProjectInline

class EventAdmin(admin.ModelAdmin):
    search_fields = ('title', 'room' , 'start' , 'spec')
    list_display = ('title', 'room' , 'start' , 'end' , 'day_index' , 'spec')

admin.site.register(models.Event , EventAdmin)
