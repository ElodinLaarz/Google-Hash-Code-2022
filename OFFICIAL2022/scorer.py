from parser import Parser

class Submission:
    def __init__(self, project_name: str, people_assigned: list, past_submissions: list, parser: Parser, day: int = 0, msg: bool = True) -> None:
        self.parser = parser
        for project_context in self.parser.projects:
            if project_context.name == project_name:
                self.context = project_context

        self.project_name = project_name
        self.past_submissions = past_submissions[::-1]
        self.people_assigned = people_assigned
        self.day = day
        self.days_to_complete = self.context.duration
        self.best_before = self.context.best_before
        self.max_score = self.context.score
        self.all_contributors = self.parser.contributors
        self.msg = msg
    
    def __str__(self) -> str:
        return f'Submission(project_name = "{self.project_name}", people_assigned = {self.people_assigned}, past_submissions = {self.past_submissions}, day = {self.day})'

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
        people_seen = set()
        for project in self.past_submissions:
            if project.day_completed <= self.day:
                #print(project.people_assigned,'BBBB')
                need_to_check -= (set(project.people_assigned) - people_seen)
            people_seen = people_seen | set(project.people_assigned)
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
                    skill_to_upgrade = project.context.roles[project.people_assigned.index(person)][0] #just in case a person has multiple skills usable in the same project, but is assigned to one
                    skill_diff = person_skills[skill_to_upgrade] - job_skills[skill_to_upgrade]
                    if skill_diff == 0 or skill_diff == -1:
                        details[person].skills[skill_to_upgrade] += 1
        return details

    def is_everyone_leveled(self) -> bool:
        details = self.level_up()
        for role, person in zip(self.context.roles, self.people_assigned):
            if not (details[person].skills[role[0]] >= role[1]-1):
                if self.msg:
                    raise ValueError(f'Contributors in project {self.project_name} not leveled enough')
                return False
            if details[person].skills[role[0]] == role[1]-1:
                if all([(details[other_person].skills.get(role[0],0) < role[1]) for other_person in self.people_assigned if person != other_person]):
                    if self.msg:
                        raise ValueError(f'{person} in project {self.project_name} not leveled enough in {role[0]} [Needed Level {role[1]}, Had Level {details[person].skills[role[0]]}]')
                    return False
        return True
    
    def day_start(self) -> None:
        while not self.is_everyone_available():
            self.day += 1

    def get_day_completed(self) -> int:
        self.day_completed = self.best_before + self.max_score
        if self.is_everyone_leveled():
            self.day_start()
            self.day_completed = self.day + self.days_to_complete
        return self.day_completed
    
    def penalty(self) -> int:
        day_completed = self.get_day_completed()
        return max(day_completed - self.best_before, 0)
    
    def score(self) -> int:
        #print(f'penalty: {self.penalty()} day completed: {self.day_completed} best before: {self.best_before}')
        return max(self.max_score - self.penalty(), 0)

class Scorer:
    def __init__(self, output_file='', input_file=''):
        self.input = input_file
        self.output = output_file
        self.parser = Parser(self.input)
    
    def score(self):
        with open(self.output,'r') as fp:
            data = [x.strip() for x in fp.readlines() if x]
        num_projects = data.pop(0)
        past_submissions = []
        score = 0
        for i in range(0, len(data), 2):
            project_name, people_assigned = data[i:i+2]
            people_assigned = people_assigned.split(' ')
            submission = Submission(project_name, people_assigned, past_submissions, self.parser)
            print(submission)
            score += submission.score()
            past_submissions.append(submission)
        return score

if __name__ == '__main__':
    file_letter = 'a'
    S = Scorer(f'./outputs/{file_letter}.out', f'./inputs/{file_letter}.in')
    print(S.score())