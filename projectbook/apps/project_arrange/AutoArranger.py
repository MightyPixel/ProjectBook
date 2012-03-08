from models import *

class AutoArranger(object):
    __max_projects = 10
    __start_hour = 8
    __commission_size = 4

    #RULES
    __respect_mentor = True
    __respect_reviewer = True

    __respect_project_categories = True
    __respect_expert_categories = True
    #ENDRULES
    
    def __dedupe(self , _list):
       return OrderedDict((item,None) for item in _list).keys()

    def reset_base(self):
        commissions = Commission.objects.all().delete()
        projects = Project.projects.get_this_year_projects().all().update(scheduled = False)
            
    def arrange_by_bussy_days(self , days , respect_mentor , respect_reviewer):
        self.reset_base()
        self.__respect_mentor = respect_mentor
        self.__respect_reviewer = respect_reviewer

        day_list = BussyDay.bussydays.get_busiest_day_for_dates(days)
        day_list += BussyDay.bussydays.get_free_days(days)
        

        day_list = self.__dedupe(sorted(day_list))
                
        self.arrange_filtered_days_for_daypart(day_list , DAY_PART_CHOICES[2])
            
        if len(Project.projects.get_this_year_projects().all().filter(scheduled = False).all()) > 0:
            self.arrange_filtered_days_for_daypart(day_list , DAY_PART_CHOICES[1])
            
        if len(Project.projects.get_this_year_projects().all().filter(scheduled = False).all()) > 0:
            self.arrange_filtered_days_for_daypart(day_list , DAY_PART_CHOICES[0])

    def arrange_filtered_days_for_daypart(self , days , part):
        assigned_days = []
        for c in Commission.objects.all():
            assigned_days.append(c.date)

        unassigned_days = [i for i in days if i not in assigned_days]

        for day in unassigned_days:
            for spec in Specialty.objects.all():
                busiest_experts = Expert.experts.get_daily_free_busiest_experts(day , days , spec)
                busiest_experts += Expert.experts.get_free_experts_for_date(day , spec)

                self.arrange_day(day , part , spec , busiest_experts)

    def arrange_day(self , day , part , spec , experts):
        if len(experts) == 0:
            return

        projects , new_commission = self.make_commission(day , part , experts , spec)

        if (projects == False) & (new_commission == False):
            return

        counter = 0
        while len(new_commission.experts.all()) < self.__commission_size:
            new_commission.experts.add(experts[counter])
            counter += 1

        self.__fill_day(day , projects , new_commission)
        
    def free_check(self , expert , day):
        commissions = Commission.objects.filter(date = day)
        for c in commissions:
            if expert in c.experts.all():
                return False
        return True

    def make_commission(self , day , daypart , experts , spec):
        new_commission = Commission(date = day , part = daypart , specialty = spec)
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
                                    if self.free_check(reviewer , day):
                                        new_commission.experts.add(mentor)
                                        new_commission.experts.add(reviewer)
                                        projects += Project.projects.get_common_projects(mentor , reviewer)
                                        projects = projects[:self.__max_projects]
        else:
            for expert in all_experts:
                if len(new_commission.experts.all()) < self.__commission_size:
                    new_commission.experts.add(expert)
            projects += Project.projects.get_this_year_projects().filter(scheduled = False).all()[:self.__max_projects]

        if len(projects) == 0:
            new_commission.delete()
            return False , False

        return projects , new_commission

    def __fill_day(self , day ,projects , commission):
        for project in projects:
            new_project = project
            new_project.commission = commission
            new_project.scheduled = True
            new_project.save()

