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


class Simulator():

    
    objects_of_note : list
    time_remaining : int
    current_file : str
    solution : list
    compiled_files : list # list[CompiledFile]
    servers : list # list[servers]

    def __init__(self, parsed_objects, current_file):
        self.objects_of_note = parsed_objects
        self.time_remaining = parsed_objects.time
        self.current_file = current_file
        self.compiled_files = parsed_obects.compiled_files
        self.servers = parsed_objects.servers

    def generate_task_requisities(self,task_name):
        requisites = []
        # Essentially BFS
        
        visited = {}
        for name in self.compiled_files:
            visited[name] = False

        remaining_files = deque()
        remaining_files.append(task_name)

        while remaining_files:
            cur_file = remaining_files.pop(0)
            requisites.append(cur_file)
            remaining_files += self.compiled_files[cur_file].dependencies
        

        return requisites[::-1]


    # Generic function for each time step
    def choice(self):
        return

    def update_solution(self):
        # Update solution list
        self.solution.append(self.time_remaining)
        return

    def time_step(self):
        if self.time_remaining == 0:
            print('Time is already up!')
            return
        self.time_remaining -= 1
        # Call all the necessary functions from here
        self.choice()
        self.update_solution()


    def create_output(self):
        with open('./outputs/' + self.current_file + '.out', w) as f:
            f.write(f'{self.time_remaining == 0}'+'\n')
            f.write(f'{self.solution}')
