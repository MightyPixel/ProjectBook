try:
    from ordereddict import OrderedDict
except ImportError:
    pass
try:
    from collections import OrderedDict
except ImportError:
    pass

from datetime import date
import itertools

from django.db.models.query import QuerySet
from django.db.models import Manager
from django.db.models import Q

import models

def common(L):
    objs_counter = dict()
    for obj in L:
        if obj in objs_counter:
            objs_counter[obj] += 1
        else:
            objs_counter[obj] = 1
    result = sorted(objs_counter, key = objs_counter.get, reverse = True)
    return result
    
def dedupe(_list):
   return OrderedDict((item,None) for item in _list).keys()

def most_common(L):
    groups = itertools.groupby(sorted(L))
    def _auxfun((item, iterable)):
        return len(list(iterable)), -L.index(item)
    return min(groups, key=_auxfun)[0]

class ProjectManager(Manager):
    def get_this_year_projects(self):
        return models.Project.objects.filter(year = date.today().year)
    
    def get_unscheduled_projects(self):
        return models.Project.objects.filter(scheduled = False)

    def get_unscheduled_projects_mentors(self):
        projects = Project.projects.get_unscheduled_projects()
        mentors = []
        for project in projects:
           mentor.append(project.mentor)
        return mentors
        
    def get_projects_for_commission(self , commission):
        projects = []
        for person in commission.experts.all():
            try:
                mentor = models.Mentor.objects.get(id = person.id)
                mentor_projects = list(models.Mentor.mentors.get_projects_of_mentor(mentor).exclude(scheduled = True))
                projects += mentor_projects
            except models.Mentor.DoesNotExist:
                pass
        return projects
    
    def get_common_projects(self , mentor , reviewer):
        print("--------------")
        print(mentor , reviewer)
        mentor_projects = dedupe(models.Expert.experts.get_projects_of_mentor(mentor).exclude(scheduled = True))
        print(mentor_projects)
        reviewer_projects = dedupe(models.Expert.experts.get_projects_of_reviewer(reviewer).exclude(scheduled = True))
        print(reviewer_projects)
        
        common_projects = set(mentor_projects).intersection(reviewer_projects)
        print(common_projects)
        
        return sorted(common_projects , key = lambda project: project.category)

class CategoryManager(Manager):
    def get_category_from_string(self , str_category):
        return models.Category.objects.get(keyword = str_category)

class PersonManager(Manager):
    def get_people_with_name(self , name):
        return models.Person.objects.filter(name = name)

class ExpertManager(Manager):
    def unpack_experts(self , all_experts):
        result = []
        mentors , reviewers , experts = [] , [] , []
        
        mentors_query = models.Expert.objects.exclude(project_mentor = None)
        reviewers_query = models.Expert.objects.exclude(project_reviewer = None)
        experts_query = models.Expert.objects.filter(project_mentor = None , project_reviewer = None)

#        print mentors_query , reviewers_query , experts_query , "QUERY"
        for expert in all_experts:
            mentors += list(mentors_query.filter(id = expert.id))
            reviewers += list(reviewers_query.filter(id = expert.id))
            experts += list(experts_query.filter(id = expert.id))            

        return mentors , reviewers , experts , all_experts
    
    def get_most_bussy_experts_for_date(self , date):
        day = models.BussyDay.objects.filter(date = date)
        expert_list = models.Expert.objects.filter(bussyday = day)
        result = common(list(expert_list))

        return result

    def get_most_bussy_experts_for_dates(self , dates):
        day_list = models.BussyDay.objects.filter(date__in = dates).all()
        expert_list = models.Expert.objects.filter(bussyday__in = day_list)
        result = common(list(expert_list))

        return result

    def get_daily_free_busiest_experts(self , date , dates , spec):
        day_list = models.BussyDay.objects.filter(date__in = dates).exclude(date = date)
        expert_list = spec.expert_set.filter(bussyday__in = day_list)
        result = common(list(expert_list))
        
        return dedupe(result)
        
        
    def get_daily_free_busiest_experts_for_part(self , date , dates , spec , part):
        day_list = models.BussyDay.objects.filter(date__in = dates).filter(date = date).exclude(part = part)
        expert_list = spec.expert_set.filter(bussyday__in = day_list)
        result = common(list(expert_list))

        return dedupe(result)

    def get_free_experts_for_date(self , date , spec):
        bussyday_list = models.BussyDay.objects.filter(date = date)
        return spec.expert_set.exclude(bussyday__in = bussyday_list)
    
    def get_free_experts_for_dates(self , dates):
        bussyday_list = models.BussyDay.objects.filter(date__in = dates)
        return models.Expert.objects.exclude(name__in = bussyday_list)
    
    def get_projects_of_mentor(self , mentor):
        return models.Project.objects.filter(mentor = mentor)

    def get_projects_of_reviewer(self , reviewer):
        projects = models.Project.objects.filter(reviewer = reviewer)
        return projects

    def get_reviewers_of_mentors_projects(self , mentor):
        reviewers = []
        projects = models.Project.objects.filter(mentor = mentor).exclude(scheduled = True)
        for project in projects:
            reviewers.append(project.reviewer)
        return reviewers

    def get_mentors_of_reviewer_projects(self , reviewer):
        mentors = []
        projects = models.Project.objects.filter(reviewer = reviewer)
        for project in projects:
            mentors.append(project.mentor)
        return mentors

class CommissionManager(Manager):
    def get_projects_count(self , commission):
        return len(models.Project.objects.filter(commission = commission))

class BussyDayManager(Manager):
    def get_busiest_day_for_dates(self , dates):
        day_list = []
        for day in dates:
            day_list.append(day)
            l = list(models.BussyDay.objects.filter(date = day))
            for item in l:
                day_list.append(item.date)
        
        return common(day_list)

    def get_busiest_day_for_dates_for_part(self , dates , part):
        day_list = []
        for day in dates:
            day_list.append(day)
            l = list(models.BussyDay.objects.filter(date = day).filter(part = part))
            for item in l:
                day_list.append(item.date)
        
        return common(day_list)

        
    def get_free_days(self , dates):
        day_list = []
        for day in dates:
            day_list.append(day)
            l = list(models.BussyDay.objects.exclude(date = day))
            for item in l:
                day_list.append(item.date)
               
        return set(sorted(day_list))

