from models import *

class AutoArranger(object):
    __max_projects = 10
    __start_hour = 8
    __commission_size = 4

    #RULES
    __respect_mentor = True
    __respect_reviewer = False

    __respect_project_categories = True
    __respect_expert_categories = True
    #ENDRULES
    
    def __dedupe(self , _list):
       return OrderedDict((item,None) for item in _list).keys()

    def reset_base(self):
        commissions = Commission.objects.all().delete()
        projects = Project.projects.get_this_year_projects().all().update(scheduled = False)
            
    def arrange_by_bussy_days(self , days):
        self.reset_base()
        day_list = BussyDay.bussydays.get_most_bussyday_for_dates(days)
        day_list += BussyDay.bussydays.get_free_days(days)
        
        for day in day_list:
            for spec in Specialty.objects.all():
                busiest_experts = Expert.experts.get_daily_free_busiest_experts(day , days , spec)
                busiest_experts += Expert.experts.get_free_experts_for_date(day , spec) 

                if len(busiest_experts) == 0:
                    continue

                projects , new_commission = self.make_commissions(day , busiest_experts , spec)

                if (projects == False) & (new_commission == False):
                    continue

                print('Projects: %s' % projects )
                print("Mentors: %s" % new_commission.experts.all())

                counter = 0
                while len(new_commission.experts.all()) < self.__commission_size:
                    new_commission.experts.add(busiest_experts[counter])
                    counter += 1

                self.__fill_day(day , projects , new_commission)

        if len(Project.projects.get_this_year_projects().all().filter(scheduled = False).all()) > 0:
            unassigned_days = []
            assigned_days = []
            for c in Commission.objects.all():
                assigned_day += c.date
           
            unassigned_days = set(days).difference(assigned_day)

            for day in day_list:
                for spec in Specialty.objects.all():
                    busiest_experts = Expert.experts.get_daily_free_busiest_experts_for_part(day , days , spec , DAY_PART_CHOICES[1])
                    busiest_experts += Expert.experts.get_free_experts_for_date(day , spec) 

                    if len(busiest_experts) == 0:
                        continue

                    projects , new_commission = self.make_commissions(day , busiest_experts , spec)

                    if (projects == False) & (new_commission == False):
                        continue

                    counter = 0
                    while len(new_commission.experts.all()) < self.__commission_size:
                        new_commission.experts.add(busiest_experts[counter])
                        counter += 1

                    self.__fill_day(day , projects , new_commission)



    def free_check(self , expert , day):
        commissions = Commission.objects.filter(date = day)
        for c in commissions:
            if expert in c.experts.all():
                return False
        return True

    def make_commissions(self , day , experts , spec):
        if len(Project.projects.get_this_year_projects().all().filter(scheduled = False).all()) > 0:
            new_commission = Commission(date = day)
            new_commission.specialty = spec
            new_commission.save()

            mentors , reviewers , experts , all_experts = Expert.experts.unpack_experts(experts)
            projects = []            

            if self.__respect_mentor == True:
                for mentor in mentors:
                    if self.free_check(mentor , day):
                        if Expert.experts.get_projects_of_mentor(mentor) == 0:
                            continue
                        project_reviewers = Expert.experts.get_reviewers_of_mentors_projects(mentor)
                        for reviewer in self.__dedupe(project_reviewers):
                            if self.__respect_reviewer == False:
                                    if len(new_commission.experts.all()) < self.__commission_size:
                                        new_commission.experts.add(mentor)
                                        projects += Expert.experts.get_projects_of_mentor(mentor)[:self.__max_projects]
                            else:
                                if reviewer in reviewers:
                                    if len(new_commission.experts.all()) < self.__commission_size-1:
                                        new_commission.experts.add(mentor)
                                        if self.free_check(mentor , day):
                                            new_commission.experts.add(reviewer)
                                            projects += Project.projects.get_common_projects(mentor , reviewer)
                                            projects = projects[:self.__max_projects]
                                                                    
                if len(projects) == 0:
                    new_commission.delete()
                    return False , False

            else:
                for expert in all_experts:
                    if len(new_commission.experts.all()) < self.__commission_size:
                        new_commission.experts.add(expert)
                projects += Project.projects.get_this_year_projects().filter(scheduled = False).all()[:self.__max_projects]

            return projects , new_commission
        else:
            return False , False

    def __fill_day(self , day ,projects , commission):
        for project in projects:
            new_project = Project.objects.get(id = project.id)
            new_project.commission = commission
            new_project.scheduled = True
            new_project.save()

#-----OTHER DEFS -------


    def arrange_projects_by_fields(self , projects , *args):
        print(args)
        sorted_projects = projects.order_by(*args)
        return self.__dedupe(sorted_projects)


    def arrange(self):
        for spec in Specialty.objects.all():
            print spec
            projects_from_spec = Project.projects.get_this_year_projects().filter(spec = spec)
            ordered_projects = self.arrange_projects_by_fields(projects_from_spec , 'mentor' , 'category')
