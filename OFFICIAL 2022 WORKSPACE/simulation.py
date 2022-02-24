from collections import deque
from dataclasses import dataclass

@dataclass
class Example:
    stuff : set

class Simulator():
    objects_of_note : list
    time_remaining : int

    def __init__(self, parsed_objects, current_hashcode_file):
        self.objects_of_note = parsed_objects
        self.time_remaining = parsed_objects.time

    def bfs(self,node_name):
        requisites = []
        # BFS
        
        visited = {}
        for name in self.compiled_files:
            visited[name] = False

        remaining_files = deque([node_name])

        while remaining_files:
            cur_file = remaining_files.popleft()
            if not visited[cur_file]:
                requisites.append(cur_file)
                remaining_files += self.compiled_files[cur_file].dependencies
                visited[cur_file] = True

        return requisites

    # Generic function for each time step
    def choice(self):
        return

    def update_solution(self):
        # Update solution list
        return

    def time_step(self):
        if self.time_remaining <= 0:
            print('Time is already up!')
            return

        self.choice()
        self.update_solution()
        self.time_remaining -= 1


    def create_output(self):
        with open('./outputs/' + self.current_hashcode_file + '.out', 'w') as f:
            f.write(f'{len(self.solution)}\n')
            for s in self.solution:
                f.write(f'{s[0]} {s[1]}\n')
