from django.contrib import admin

from models import ArchiveCategory

from models import SchoolYear
from models import ArchiveStudent
from models import ArchiveExpert

from models import ArchiveSpecialty
from models import ArchiveSchoolClass

from models import ArchiveDiplomaWork
from models import ArchiveProject
from models import ArchiveCommission

class ArchiveProjectInline(admin.TabularInline):
    pass

class ArchiveCategoryAdmin(admin.ModelAdmin):
    pass
        
class ArchiveStudentAdmin(admin.ModelAdmin):
    pass

class ArchiveExpertAdmin(admin.ModelAdmin):
    pass
    
class ArchiveSpecialtyAdmin(admin.ModelAdmin):
    pass

class ArchiveSchoolClassAdmin(admin.ModelAdmin):
    pass

class ArchiveDiplomaWorkAdmin(admin.ModelAdmin):
    pass
class ArchiveProjectAdmin(admin.ModelAdmin):
    pass


class BussyDayAdmin(admin.ModelAdmin):
    pass
class ArchiveCommissionAdmin(admin.ModelAdmin):
    pass

admin.site.register(SchoolYear)
admin.site.register(ArchiveCategory , ArchiveCategoryAdmin)

admin.site.register(ArchiveStudent , ArchiveStudentAdmin)
admin.site.register(ArchiveExpert , ArchiveExpertAdmin)
admin.site.register(ArchiveSpecialty , ArchiveSpecialtyAdmin)
admin.site.register(ArchiveSchoolClass , ArchiveSchoolClassAdmin)

admin.site.register(ArchiveDiplomaWork , ArchiveDiplomaWorkAdmin)
admin.site.register(ArchiveProject , ArchiveProjectAdmin)
admin.site.register(ArchiveCommission , ArchiveCommissionAdmin)





