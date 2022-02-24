from dataclasses import dataclass
from parser import Parser, Project

@dataclass
class Submission:
    project_name: str
    past_submissions: list
    people_assigned: list
    day: int
    days_to_complete: int
    best_before: int
    max_score: int
    context: Project
    all_contributors: list

    def get_contributor_details(self) -> dict:
        contribs = {}
        for person in self.people_assigned:
            for contributor in self.all_contributors:
                if person == contributor.name:
                    contribs[person] = contributor
        return contribs


    def get_new_contributors(self) -> set:
        need_to_check = set(self.people_assigned)
        for project in self.past_submissions:
            need_to_check -= set(project.people_assigned)
        return need_to_check

    def is_everyone_available(self) -> bool:
        need_to_check = set(self.people_assigned)
        need_to_check -= self.get_new_contributors()
        for project in self.past_submissions:
            #print(project.day_completed, self.day)
            if project.day_completed <= self.day:
                #print(project.people_assigned,'BBBB')
                need_to_check -= set(project.people_assigned)
        if len(need_to_check) > 0:
            #print(need_to_check)
            return False
        return True
    
    def level_up(self) -> dict:
        details = self.get_contributor_details()
        for project in self.past_submissions[::-1]:
            for person in self.people_assigned:
                if person in project.people_assigned:
                    person_skills = details[person].skills
                    job_skills = dict(project.context.roles)
                    skill_to_upgrade = (person_skills.keys()&job_skills.keys()).pop()
                    skill_diff = person_skills[skill_to_upgrade] - job_skills[skill_to_upgrade]
                    if skill_diff == 0 or skill_diff == -1:
                        details[person].skills[skill_to_upgrade] += 1
        return details

    def is_everyone_leveled(self) -> bool:
        details = self.level_up()
        failed = False
        for role, person in zip(self.context.roles, self.people_assigned):
            #print(details[person].skills[role[0]])
            #print(self.project_name, person, role[0], details[person].skills[role[0]], role[1])
            if not (details[person].skills[role[0]] >= role[1]-1):
                failed = True
        return not failed
    
    def day_start(self) -> None:
        while not self.is_everyone_available():
            self.day += 1
        if not self.is_everyone_leveled():
            raise ValueError(f'Contributors in project {self.project_name} not levelled enough')

    def get_day_completed(self) -> int:
        self.day_start()
        self.day_completed = self.day + self.days_to_complete
        return self.day_completed
    
    def penalty(self) -> int:
        day_completed = self.get_day_completed()
        return max(day_completed - self.best_before, 0)
    
    def score(self) -> int:
        return max(self.max_score - self.penalty(), 0)

class Scorer:
    def __init__(self, output_file, input_file):
        self.input = input_file
        self.output = output_file
        self.A = Parser(self.input)
    
    def score(self):
        with open(self.output,'r') as fp:
            data = [x.strip() for x in fp.readlines() if x]
        num_projects = data.pop(0)
        all_contributors = self.A.contributors
        submissions = []
        score = 0
        for i in range(0, len(data), 2):
            project_name, contributors = data[i:i+2]
            for p in self.A.projects:
                if p.name == project_name:
                    days_to_complete = p.duration
                    day = 0
                    best_before = p.best_before
                    max_score = p.score
                    project_context = p
            
            submission = Submission(project_name, submissions[::-1], contributors.split(' '), day, days_to_complete, best_before, max_score, project_context, all_contributors)
            #print(submission)
            score += submission.score()
            submissions.append(submission)
        return score
        