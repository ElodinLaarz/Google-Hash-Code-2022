"""
Goal of this simulator is to see what are the bounds on how fast a
task can be completed.

We do this by first answering the following:
    Using all available servers, how long does it take?
Then, we see how long it takes with s-1 servers, s-2, etc. until
either the task is completed with 1 server or the the task is impossiblewith the given number of servers.

There is a bit of choice that we make when assigning the servers, but
we take a 'greedy' sort of approach where a server chooses to compile whatever necessary task is available that is currently going to take the longest amount of t
"""
from collections import deque
from dataclasses import dataclass
from http.client import REQUEST_URI_TOO_LONG

from isort import file

@dataclass
class Server:
    server_files : set
    busy_until : int = 0
    cur_compiling : str = ""

class Simulator():
    # objects_of_note : list
    current_hashcode_file : str
    compiled_files : dict
    servers : list # list[servers]
    goal : str
    files_to_reach_goal : list = []
    solution : list = []
    goal_attained : bool = False
    currently_replicating : set = set()
    latest_deadline : int = -1
    current_time : int = 0
    globally_available_files : dict  = {}
    replicated : dict = {}

    def __init__(self, parsed_objects, current_hashcode_file):
        # self.objects_of_note = parsed_objects
        # self.time_remaining = parsed_objects.time
        self.current_hashcode_file = current_hashcode_file
        self.compiled_files = parsed_objects.compiled_files
        self.target_file_names = []
        for file_name in self.compiled_files:
            if self.compiled_files[file_name].TARGET_FILE:
                self.target_file_names.append(file_name)
                if self.compiled_files[file_name].DEADLINE > self.latest_deadline:
                    self.latest_deadline = self.compiled_files[file_name].DEADLINE
            if not self.compiled_files[file_name].dependencies:
                self.globally_available_files[file_name] = True
                self.replicated[file_name] = True
            else:
                self.globally_available_files[file_name] = False
                self.replicated[file_name] = False
        
        self.servers = [Server(set()) for i in range(parsed_objects.n_servers)]

    def generate_task_requisities(self,task_name):
        requisites = []
        # Essentially BFS
        
        visited = {}
        for name in self.compiled_files:
            visited[name] = False

        remaining_files = deque([task_name])

        while remaining_files:
            cur_file = remaining_files.popleft()
            if not visited[cur_file]:
                requisites.append(cur_file)
                remaining_files += self.compiled_files[cur_file].dependencies
                visited[cur_file] = True

        return requisites[::-1]


    # Generic function for each time step
    def choice(self, server_index):
        for i, file_name in enumerate(self.files_to_reach_goal):
            if all(self.globally_available_files[x] or x in self.servers[server_index].server_files for x in self.compiled_files[file_name].dependencies):
                # print(f'Compiled {file_name} on {server_index}')
                self.files_to_reach_goal.pop(i)
                self.solution.append((file_name, server_index))
                self.servers[server_index].cur_compiling = file_name
                self.servers[server_index].busy_until = self.current_time + self.compiled_files[file_name].C
                self.servers[server_index].server_files.add(file_name)
                return

    def set_goal(self, goal):
        self.goal = goal
        self.files_to_reach_goal = self.generate_task_requisities(goal)

    def update_solution(self):
        # Update solution list
        return

    def replicate(self, file_name):
        if file_name == '':
            return
        else:
            if not self.replicated[file_name]:
                self.currently_replicating.add((file_name,self.current_time+self.compiled_files[file_name].R))
                self.replicated[file_name] = True

    def check_replications(self):
        to_remove = []
        for (file_name, replication_time) in self.currently_replicating:
            if self.current_time >= replication_time:
                self.globally_available_files[file_name] = True
                to_remove.append((file_name, replication_time))
            
        for pair in to_remove:
            self.currently_replicating.remove(pair)

    def check_goal(self):
        self.goal_attained = self.replicated[self.goal]


    def time_step(self):
        if self.current_time > self.latest_deadline:
            print('Time is already up!')

        for i, server in enumerate(self.servers):
            if self.current_time >= server.busy_until:
                self.replicate(server.cur_compiling)
                self.choice(i)
        self.check_replications()
        self.check_goal()
        self.current_time += 1


    def create_output(self):
        with open('./outputs/' + self.current_hashcode_file + '.out', 'w') as f:
            f.write(f'{len(self.solution)}\n')
            for s in self.solution:
                f.write(f'{s[0]} {s[1]}\n')
