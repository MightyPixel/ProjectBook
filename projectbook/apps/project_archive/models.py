
from datetime import date

from django.db import models

class SchoolYear(models.Model):
    year = models.IntegerField(default=date.today().year)

class ArchivePerson(models.Model):
    name = models.CharField(max_length = 255)
    email = models.CharField(max_length = 255 , blank = True , null = True)
    number = models.CharField(max_length = 15 , blank = True , null = True)

    def Meta(self):
        abstract = True
    
    def __unicode__(self):
        return  self.name

class ArchiveStudent(ArchivePerson):
    school_class = models.ForeignKey('ArchiveSchoolClass')
    diploma_work = models.OneToOneField('ArchiveDiplomaWork')

class ArchiveExpert(ArchivePerson):
    year = models.ForeignKey(SchoolYear)
    category = models.ManyToManyField('ArchiveCategory' , blank = True )

    specilties = models.ManyToManyField('ArchiveSpecialty' , blank = True , null = True)

    def category_names(self):
        return ', '.join([c.keyword for c in self.category.all()])
    category_names.short_description = "Categories"

    def specities_names(self):
        return ', '.join([s.get_spec_type_display() for s in self.specilties.all()])
    specities_names.short_description = "Specities"
########################################################
#
########################################################
class ArchiveCategory(models.Model):
    year = models.ForeignKey(SchoolYear)
    keyword = models.CharField(max_length = 125 , unique=True , help_text="enter IT category")

    class Meta:
        ordering = ['keyword']

    def __unicode__(self):
        return self.keyword


class ArchiveSpecialty(models.Model):
    SPECIALTY_CHOICES = (
        (u'hw' , u'Hardware'),
        (u'sw' , u'Software'),
        (u'nw' , u'Network'),
    )
    year = models.ForeignKey(SchoolYear)
    spec_type = models.CharField(max_length = 3 ,
                                 choices = SPECIALTY_CHOICES,
                                 unique = True)
    room = models.CharField(max_length = 5 , blank=True , null=True)

    def __unicode__(self):
        return self.get_spec_type_display()

DAY_PART_CHOICES = (
    (u"m" , u"Morning"),
    (u"n" , u"After Noon"),
    (u"d" , u"All Day"),
)

class ArchiveCommission(models.Model):
    year = models.ForeignKey(SchoolYear)
    date = models.DateField()
    part = models.CharField(max_length = 3 , choices = DAY_PART_CHOICES , default = DAY_PART_CHOICES[1])

    experts = models.ManyToManyField(ArchiveExpert)
    
    category = models.ManyToManyField(ArchiveCategory , blank = True , null = True)
    specialty = models.ForeignKey('ArchiveSpecialty' , null = True)

    def expert_names(self):
        return ', '.join([e.name for e in self.experts.all()])
    expert_names.short_description = "Experts"

    def __unicode__(self):
        return "%s: %s -> %s " % ( self.specialty , self.date , self.expert_names())


class ArchiveSchoolClass(models.Model):
    year = models.ForeignKey(SchoolYear)
    grade = models.CharField(max_length = 1)
    speciality = models.ForeignKey(ArchiveSpecialty)

    def __unicode__(self):
        return "%s - %s - %s" % (self.grade , self.speciality , self.year)

class ArchiveProject(models.Model):
    year = models.ForeignKey(SchoolYear)
    title = models.CharField(max_length=255)
    category = models.ManyToManyField(ArchiveCategory , blank=True)

    commission = models.ForeignKey(ArchiveCommission , blank = True , null = True , on_delete=models.SET_NULL)
    mentor = models.ForeignKey(ArchiveExpert , related_name="project_mentor" )
    reviewer = models.ForeignKey(ArchiveExpert , related_name="project_reviewer")

    def category_names(self):
        return ', '.join([c.keyword for c in self.category.all()])
    category_names.short_description = "Categories"

    def __unicode__(self):
        return self.title

class ArchiveDiplomaWork(models.Model):
    completed = models.BooleanField(default = False)
    project = models.ForeignKey(ArchiveProject)
    
    def __unicode__(self):
        return "%s -completed? %s" % (self.project.title , self.completed) 
