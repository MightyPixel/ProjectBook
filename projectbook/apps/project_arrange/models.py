from ordereddict import OrderedDict
from datetime import date

from django.db import models

import managers

class Person(models.Model):
    """
    Abstract class
    The base class for every student; teacher; mentor; reviewer etc.
    Contains fields
        - name : name of the person
        - email : e-mail of the person
        - number : telephone number    
    """
    name = models.CharField(max_length = 255)
    email = models.CharField(max_length = 255 , blank = True , null = True)
    number = models.CharField(max_length = 15 , blank = True , null = True)    
    
    people = managers.PersonManager()
    objects = models.Manager()
    
    def Meta(self):
        abstract = True
    
    def __unicode__(self):
        return  self.name

class Student(Person):
    """
    Student represents creator of target project
    Contains fields
        - school_class : class of the school
        - diploma_work : one to one relation to part(whole) project
    """
    school_class = models.ForeignKey('SchoolClass')
    diploma_work = models.OneToOneField('DiplomaWork')

class Expert(Person):
    """
    Expert is the base class for every person in target commission.
    Un expert can have 
    days in which he is busy,
    so he can't be part of commission.
    Every expert have optimal categories in which he is expert at.
    The categories help for arranging projects.
    
    >>> e = Expert()    
    >>> e.name = "Test"
    >>> e.email = "test@test.com"
    >>> e.number = "000000000"
    >>> c = Category.objects.get(id=1)
    >>> e.save()
    >>> e.category.add(c)
    >>> print e
    Test
    >>> print e.category.all()[0]
    Test Application
    """
    category = models.ManyToManyField('Category' , blank = True )

    specilties = models.ManyToManyField('Specialty' , blank = True , null = True)

    experts = managers.ExpertManager()
    objects = models.Manager()

    def category_names(self):
        return ', '.join([c.keyword for c in self.category.all()])
    category_names.short_description = "Categories"

    def specities_names(self):
        return ', '.join([s.get_spec_type_display() for s in self.specilties.all()])
    specities_names.short_description = "Specities"

    def is_bussy(self , day):
        return bool(BussyDay.object.filter(date = day , expert = self))
########################################################
#
########################################################
class Category(models.Model):
    """
    Category represents the category which target Expert is expert at
    and target Project category
    Contains keyword like : Web Application , Desctop Application , Cisco
    The Categories are added from admin
    >>> c = Category()
    >>> c.keyword = "Test Application"
    >>> c.save()
    >>> print c.keyword
    Test Application
    """
    keyword = models.CharField(max_length = 125 , unique=True , help_text="enter IT category")
    categories = managers.CategoryManager()
    objects = models.Manager()

    class Meta:
        ordering = ['keyword']

    def __unicode__(self):
        return self.keyword


class Specialty(models.Model):
    """
    The specialities in which projects can be created
    The Specialty types are Software, Hardware and Network
    The admin can modify the system by adding additional field like so:
    >>> s = Specialty()
    >>> s.spec_type = Specialty.SPECIALTY_CHOICES[1][0]
    >>> s.save()
    >>> print s
    Software
    """
    SPECIALTY_CHOICES = (
        (u'hw' , u'Hardware'),
        (u'sw' , u'Software'),
        (u'nw' , u'Network'),
    )
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

class Commission(models.Model):
    date = models.DateField()
    part = models.CharField(max_length = 3 , choices = DAY_PART_CHOICES , blank=True , null=True)

    experts = models.ManyToManyField(Expert)
    
    category = models.ManyToManyField(Category , blank = True , null = True)
    specialty = models.ForeignKey('Specialty' , null = True)

    commissions = managers.CommissionManager()
    objects = models.Manager()

    def is_upcoming(self):
        return date.year >= datetime.today().year

    def expert_names(self):
        return ', '.join([e.name for e in self.experts.all()])
    expert_names.short_description = "Experts"

    def __unicode__(self):
        return "%s: %s -> %s " % ( self.specialty , self.date , self.expert_names())

class BussyDay(models.Model):
    """
    Day in which target Expert is busy.
    Contains fields
        - date : the date in which the Expert is busy
        - day_part : the part of the day in which the Expert is busy
    """
    expert = models.ForeignKey(Expert)
    
    date = models.DateField()
    part = models.CharField(max_length = 3 , choices = DAY_PART_CHOICES )

    bussydays = managers.BussyDayManager()
    objects = models.Manager()

    def __unicode__(self):
        return "%s - %s" % (self.date , self.get_part_display())


class SchoolClass(models.Model):
    """
    SchoolClass represents the diftent class in target school
    Contains
        -grade : A , B , V , G
        -speciality : field to target Specialty
    >>> s = SchoolClass()
    >>> s.grade = 'A'
    >>> s.speciality = Specialty.objects.get(id=1)
    >>> s.save()
    >>> print s.grade
    A
    >>> print s.speciality
    Hardware
    """
    grade = models.CharField(max_length = 1)
    speciality = models.ForeignKey(Specialty)
    year = models.IntegerField(default=date.today().year)

    def is_upcoming(self):
        return self.year >= date.today().year

    def __unicode__(self):
        return "%s - %s - %s" % (self.grade , self.speciality , self.year)

class Project(models.Model):
    year = models.IntegerField(default=date.today().year)
    
    scheduled = models.BooleanField(default = False)

    title = models.CharField(max_length=255)
    category = models.ManyToManyField(Category , blank=True)

    commission = models.ForeignKey(Commission , blank = True , null = True , on_delete=models.SET_NULL)
    mentor = models.ForeignKey(Expert , related_name="project_mentor" )
    reviewer = models.ForeignKey(Expert , related_name="project_reviewer")

    projects = managers.ProjectManager()
    objects = models.Manager()

    def category_names(self):
        return ', '.join([c.keyword for c in self.category.all()])
    category_names.short_description = "Categories"

    def __unicode__(self):
        return self.title

class DiplomaWork(models.Model):
    completed = models.BooleanField(default = False)
    project = models.ForeignKey(Project)
    
    def __unicode__(self):
        return "%s -completed? %s" % (self.project.title , self.completed)     


