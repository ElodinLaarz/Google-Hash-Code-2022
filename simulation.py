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

    # Generic function for each time step
    def choice(self):
        # Choose what to do at some time increment
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
