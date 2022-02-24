import inspect
import os
from collections import defaultdict

class Contributor:
    def __init__(self, name, n_skills, skills):
        self.name = name
        self.n_skills = n_skills
        self.skills = skills
    
    def __repr__(self):
        R = []
        for ele in inspect.getmembers(self):      
            if not ele[0].startswith('_') and not ele[0].endswith('_'):
                if not inspect.ismethod(ele[1]): 
                    R.append((ele[0], ele[1]))
        return str(R)

class Project:
    def __init__(self, name, duration, score, best_before, n_roles, roles):
        self.name = name
        self.duration = duration
        self.score = score
        self.best_before = best_before
        self.n_roles = n_roles
        self.roles = roles

    def __repr__(self):
        R = []
        for ele in inspect.getmembers(self):      
            if not ele[0].startswith('_') and not ele[0].endswith('_'):
                if not inspect.ismethod(ele[1]): 
                    R.append((ele[0], ele[1]))
        return str(R)

class Parser: 
    def __init__(self, filename):
        self.filename = filename
        self.content = open(filename, 'r').readlines()
        self.parse()

    def parse(self):
        # line one content
        content = [int(ele) for ele in self.content[0].split()]
        self.n_contributors = content[0]
        self.C = content[0]
        self.n_projects = content[1]
        self.P = content[1]       
        self.contributors = []
        self.skills = []
        self.projects = []

        # next C group of lines
        cc = 0
        self.att_name = [] # or dict() or tuple()
        for i in range(self.C):
            # line = cc + 1 
            name = self.content[cc + 1].split()[0]
            n_skills = int(self.content[cc + 1].split()[1])
            skills = dict()
            for j in range(n_skills):
                # line = cc + 2 + j
                skill = self.content[cc + 2 + j].split()[0]
                level = int(self.content[cc + 2 + j].split()[1])
                skills[skill] = level
                self.skills.append(skill)
            
            cc += 1 + n_skills
            self.contributors.append(Contributor(name, n_skills, skills))
        self.contributors_dict = {cont.name: cont for cont in self.contributors} 

        self.skills = sorted(list(set(self.skills)))

        self.skills_dict = {skill: [] for skill in self.skills}
        for cont in self.contributors:
            for skill in cont.skills:
                self.skills_dict[skill].append(cont)
        
        # next 2*P lines
        self.projects = []
        for i in range(self.P):
            # line = cc + 1
            content = self.content[cc + 1].split()
            name = content[0]
            duration = int(content[1])
            score = int(content[2])
            best_before = int(content[3])
            n_roles = int(content[4])
            roles = []
            for j in range(n_roles):
                # line = cc + 2 + j
                skill = self.content[cc + 2 + j].split()[0]
                level = int(self.content[cc + 2 + j].split()[1])
                roles.append((skill, level))
            cc += 1 + n_roles
            self.projects.append(Project(
                name, duration, score, best_before, n_roles, roles))

        self.projects_dict = {proj.name: proj for proj in self.projects}

    def max_required(self):
        self.initial_fails = dict()
        for skill in self.skills:
            best = 0
            for cont in self.contributors:
                if skill in cont.skills:
                    best = max([best, cont.skills[skill]])
            initial_fails = []
            for proj in self.projects:
                project_initial_fails = []
                for req_skill, req_level in proj.roles:
                    if req_skill == skill:
                        if req_level > best:
                            initial_fails.append((proj, skill, req_level))
                            project_initial_fails.append((skill, req_level))
                setattr(proj, 'initial_fails', project_initial_fails)
                setattr(proj, 'n_initial_fails', len(project_initial_fails))
            self.initial_fails[skill] = initial_fails

    def sort_projects(self):
        self.max_required()
        projects = [
            (
                proj.name,
                proj.n_initial_fails,
                proj.n_roles,
                proj.score + proj.best_before,
                proj.score
            )
            for proj in self.projects
        ]
        projects.sort(key = lambda x: x[1] * 10**12 + x[2] * 10**6 + x[3])
        self.sorted_projects = projects
        return projects



    def print_dir(self):
        print(self.filename)
        D = {'methods': [], 'attributes': []}
        for ele in inspect.getmembers(self):      
            if not ele[0].startswith('_') and not ele[0].endswith('_'):
                if not inspect.ismethod(ele[1]): 
                    name = ele[0]
                    if name not in ['content', 'filename'] and hasattr(ele[1], '__iter__'):
                        name += f"({type(ele[1])})"
                        if isinstance(ele[1], dict):
                            key = list(ele[1].keys())[0]
                            print(f'attribute {ele[0]} has {len(ele[1])} elements like {key} -> {ele[1][key]}')
                        elif isinstance(ele[1], list) or isinstance(ele[1], tuple):
                            print(f'attribute {ele[0]} has {len(ele[1])} elements like {ele[1][0]}')
                    D['attributes'].append(name)
                else:
                    D['methods'].append(ele[0])
        for key in D:
            print(key, D[key])
