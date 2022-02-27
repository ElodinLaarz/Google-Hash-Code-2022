import random

from collections import deque
from dataclasses import dataclass

class Simulator():
    # projects_assigned : int = 0
    # skills : list = []
    # projects : list = []
    # ongoing_projects : list = []
    # contributors : list = []
    # free_contributors : set = set()
    # current_time : int = 0
    # done : bool = False
    # solution : list = []
    
    def __init__(self, parsed_objects, current_hashcode_file):
        self.current_hashcode_file = current_hashcode_file
        self.skills = parsed_objects.skills
        self.contributors = parsed_objects.contributors
        self.free_contributors = set()
        for contributor in self.contributors:
            self.free_contributors.add(contributor.name)
        self.projects = parsed_objects.projects
        self.ongoing_projects = []
        self.current_time = 0
        self.done = False
        self.solution = []

    def check_team(self, project_roles_levels, team):
        for role, team_member in zip(project_roles_levels, team):
            skill_name = role[0]
            skill_level = role[1]
            
            team_member_skill_level = team_member.skills.get(skill_name, 0)

            if team_member_skill_level < skill_level-1:
                return False
            if team_member_skill_level == skill_level-1:
                has_mentor = False
                for other_member in team:
                    if other_member.skills.get(skill_name, 0) >= skill_level:
                        has_mentor = True
                        break
                if not has_mentor:
                    return False
        return True

    def free_team(self, index):
        project_to_free = self.ongoing_projects[index]
        team_to_free = project_to_free[0]
        project_roles = project_to_free[3]

        # Improve skills of mentored humans
        for member, role in zip(team_to_free, project_roles):
            skill_name = role[0]
            skill_level = role[1]
            cur_skill_level = member.skills.get(skill_name, 0)
            if cur_skill_level <= skill_level:
                member.skills[skill_name] = cur_skill_level + 1            
        
        member_names = [x.name for x in team_to_free]
        for member_name in member_names:
            self.free_contributors.add(member_name)

    def assign_team(self, team, project):
        # for member in team:
        #     self.free_contributors.remove(member.name)
        
        self.projects.remove(project)
        project_end_time = self.current_time + project.duration
        project_name = project.name
        project_roles = project.roles
        self.ongoing_projects.append((team, project_end_time, project_name, project_roles))
        self.ongoing_projects.sort(key = lambda x: x[1])
        member_names = [x.name for x in team]
        self.solution.append((project_name, member_names))

    def team_exists(self, project_roles_levels, role_index = 0, team = []):
        """
        project_roles_levels : list[tuple]
        e.g. [('HTML', 3), ('C++', 2)]

        role_index : int
        index of the role in recursion that we're currently trying to fill

        team : list(contributors)
        The current team that we've assembled so far.
        """
        if role_index == 0:
            team = []
        if role_index >= len(project_roles_levels):
            valid_team = self.check_team(project_roles_levels, team)
            if valid_team:
                return team
            else:
                return []
        else:
            skill_name = project_roles_levels[role_index][0]
            skill_level = project_roles_levels[role_index][1]
            # add someone to the team who is capable or could use a mentor.
            possible_members = [x for x in self.contributors if x.name in self.free_contributors and
                                x.skills.get(skill_name, 0) >= skill_level-1]
            # print(f'Choosing a possible member for {skill_name} amongst {len(possible_members)} many members.')
            for member in possible_members:
                team.append(member)
                self.free_contributors.remove(member.name)
                if self.team_exists(project_roles_levels, role_index+1, team):
                    return team
                team.pop()
                self.free_contributors.add(member.name)
            # print('no team was possible')
            return []

    def shuffle_projects(self):
        random.shuffle(self.projects)

    def time_step(self):
        if self.current_time == 0:
            self.shuffle_projects()
        
        for i, project in enumerate(self.projects):
            project_team = self.team_exists(project.roles)
            if project_team:
                # print(f'We assigned {[(x.name, x.skills) for x in project_team]} to {project.roles}.')
                self.assign_team(project_team, project)
        
        newly_free_member = False
        projects_freed = 0
        for i in range(len(self.ongoing_projects)):
            project_end_time = self.ongoing_projects[i][1]
            if project_end_time <= self.current_time:
                newly_free_member = True
                self.free_team(i)
                projects_freed += 1
        
        self.ongoing_projects = self.ongoing_projects[projects_freed:]
        
        all_projects_are_ongoing = [x[1] > self.current_time for x in self.ongoing_projects]

        # print(all_projects_are_ongoing)
        assert(all(all_projects_are_ongoing) or not all_projects_are_ongoing)
        if not self.ongoing_projects:
            if not newly_free_member:
                self.done = True
        else:
            # Set time to completion of next project
            self.current_time = self.ongoing_projects[0][1]

    def create_output(self):
        with open('./outputs/' + self.current_hashcode_file + '.out', 'w') as f:
            f.write(f'{len(self.solution)}\n')
            for s in self.solution:
                f.write(f'{s[0]}\n')
                f.write(f'{" ".join(s[1])}\n')
