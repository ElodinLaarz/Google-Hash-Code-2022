from collections import deque
from dataclasses import dataclass

class Simulator():
    current_time : int
    skills : list
    projects : list
    contributors : list
    contributors_by_skill : dict
    free_contributors : set
    done : bool = False 
    solution : list = []
    team_free_at : list = []

    def free_team(self,team):
        return


    def assign_team(self, team, project):
        return

    def team_exists(self, project_roles, role_index = 0, members = []):
        return

    def __init__(self, parsed_objects, current_hashcode_file):
        self.current_hashcode_file = current_hashcode_file
        self.free_contributors = set()
        self.skills = parsed_objects.skills
        self.contributors = parsed_objects.contributors
        for contributor in self.contributors:
            self.free_contributors.add(contributor.name)
        self.projects = parsed_objects.projects

    def time_step(self):

        self.current_time += 1

    def create_output(self):
        with open('./outputs/' + self.current_hashcode_file + '.out', 'w') as f:
            f.write(f'{len(self.solution)}\n')
            for s in self.solution:
                f.write(f'{s[0]}\n')
                f.write(f'{" ".join(s[1])}\n')
