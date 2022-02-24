from collections import deque
from dataclasses import dataclass

@dataclass
class Example:
    stuff : set

class Simulator():
    current_time : int
    skills : list
    projects : list
    contributors : list
    contributors_by_skill : dict
    free_contributors : set 
    solution : list = []
    team_free_at : list = []

    def free_team(self,team):
        for contributor in team:
            self.free_contributors.add(contributor)


    def assign_team(self, team, project):
        self.solution.append([project.name, team])
        for contributor in team:
            self.free_contributors.remove(contributor)

    def team_exists(self, project_roles, role_index = 0, members = []):
        if role_index < len(project_roles):
            cur_skill_needed = project_roles[role_index]

            # iterate over free members who have the desired skill
            for index, contributor in enumerate(list(filter(lambda x : x.name in self.free_contributors and x.skills[project_roles[0]] >= project_roles[1], self.contributors_by_skill[cur_skill_needed]))):
                members.append(contributor)
                new_members = self.team_exists(project_roles, role_index=role_index+1, members=members)
                if len(new_members) == len(project_roles):
                    return new_members
                else:
                    members.pop()
            
            return []
        else:
            return members

    def __init__(self, parsed_objects, current_hashcode_file):
        self.free_contributors = set()
        self.skills = parsed_objects.skills
        self.contributors = parsed_objects.contributors
        for contributor in self.contributors:
            self.free_contributors.add(contributor.name)
        for skill in self.skills:
            self.contributors_by_skill[skill] = []
            for contributor in self.contributors:
                if contributor.skills[skill] > 0:
                    self.contributors_by_skill[skill].append(contributor)
        self.projects = parsed_objects.projects
        self.time_remaining = parsed_objects.time

    def time_step(self):

        for project in self.projects:
            team = self.team_exists(project.roles)
            if team:
                self.projects.remove(project)
                self.assign_team(team, project)
                self.team_free_at.append((team, project.duration))
        
        for (team, free_time) in self.team_free_at:
            if free_time >= self.current_time:
                self.free_team(team)

        self.current_time += 1


    def create_output(self):
        with open('./outputs/' + self.current_hashcode_file + '.out', 'w') as f:
            f.write(f'{len(self.solution)}\n')
            for s in self.solution:
                f.write(f'{s[0]}\n')
                for _ in s[1]:
                    f.write(f'{_} ')
                f.write('\n')
