from django.contrib import admin

from models import Category

from models import Student
from models import Expert

from models import Specialty
from models import SchoolClass

from models import DiplomaWork
from models import Project
from models import BussyDay
from models import Commission

class ProjectInline(admin.TabularInline):
    model = Project

class BussyInline(admin.StackedInline):
    model = BussyDay
    extra = 1

class CategoryAdmin(admin.ModelAdmin):
    search_fields = ('category',)
        
class StudentAdmin(admin.ModelAdmin):
    search_fields = ('name',)
    list_display = ('name' , 'email' , 'number' , 'school_class' , 'diploma_work')
    list_filter = ('school_class' ,)

class ExpertAdmin(admin.ModelAdmin):
    search_fields = ('name',)
    list_display = ('name' , 'email' , 'number' , 'specities_names')
    inlines = [BussyInline]
    filter_horizontal = ('category' , 'specilties')
    
class SpecialtyAdmin(admin.ModelAdmin):
    pass

class SchoolClassAdmin(admin.ModelAdmin):
    search_fields = ('speciality' , 'year', )
    list_display = ( 'grade' , 'speciality' , 'year', )
    list_filter = ( 'grade' , 'speciality' , 'year', )

def make_completed(modeladmin, request, queryset):
    queryset.update(completed=True)
make_completed.short_description = "Mark selected stories as completed"

def make_uncompleted(modeladmin, request, queryset):
    queryset.update(completed=False)
make_uncompleted.short_description = "Mark selected stories as uncompleted"

class DiplomaWorkAdmin(admin.ModelAdmin):
    actions = [make_completed , make_uncompleted]
    list_display = ('completed' , 'project')
    list_display_links = ('project',)
    list_editable = ('completed' ,)

def make_scheduled(modeladmin, request, queryset):
    queryset.update(scheduled=True)
make_scheduled.short_description = "Mark selected projects as scheduled"

def make_unscheduled(modeladmin, request, queryset):
    queryset.update(scheduled=False)
make_unscheduled.short_description = "Mark selected projects as unscheduled"

def unassign_commission(modeladmin, request, queryset):
    queryset.update(commission=None)
unassign_commission.short_description = "Unassign selected projects without commission"

class ProjectAdmin(admin.ModelAdmin):
    actions = [make_scheduled , make_unscheduled , unassign_commission]

    search_fields = ('title' , 'mentor' , 'reviewer',)
    list_display = ('title',
                    'scheduled',
                    'mentor',
                    'reviewer',
                    'commission',
                    'category_names')
    list_filter = ('scheduled' , 'mentor' , 'reviewer')
    filter_horizontal = ('category' ,)
    list_editable = ('commission' ,)


class BussyDayAdmin(admin.ModelAdmin):
    list_display = ('date' , 'expert')
    list_filter = ('date' , 'expert')
    
class CommissionAdmin(admin.ModelAdmin):
    search_fields = ('mentor' , 'reviewer')
    filter_horizontal = ('category' , 'experts')
    inlines = [ProjectInline]

admin.site.register(Category , CategoryAdmin)

admin.site.register(Student , StudentAdmin)
admin.site.register(Expert , ExpertAdmin)
admin.site.register(Specialty , SpecialtyAdmin)
admin.site.register(SchoolClass , SchoolClassAdmin)

admin.site.register(DiplomaWork , DiplomaWorkAdmin)
admin.site.register(Project , ProjectAdmin)
admin.site.register(BussyDay , BussyDayAdmin)
admin.site.register(Commission , CommissionAdmin)





