import argparse
import inspect
import os
import pickle

def arguments():
    parser = argparse.ArgumentParser(description='Get(s) the path to input files')
    parser.add_argument('--root', '-r', type=str, default=None)
    parser.add_argument('--path', '-p', type=str, default=None)
    return parser.parse_args()


class Server:
    def __init__(self, i):
        self.name = f"Server{i}"
        self.server_files : []

    def __repr__(self):
        R = []
        for ele in inspect.getmembers(self):      
            if not ele[0].startswith('_') and not ele[0].endswith('_'):
                if not inspect.ismethod(ele[1]): 
                    R.append((ele[0], ele[1]))
        return str(R)

class CompiledFile:
    def __init__(self, name, compile_time, replication_time):
        self.name = name
        self.compile_time = compile_time
        self.C = compile_time
        self.replication_time = replication_time
        self.R = replication_time
        self.n_dependencies = 0
        self.dependencies = []
        self.TARGET_FILE = False
        self.DEADLINE = 0
        self.GOAL_POINTS = 0

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
        self.n_compiled = content[0]
        self.C = content[0]
        self.n_targets = content[1]
        self.T = content[1] 
        self.n_servers = content[2]
        self.S = content[2]
      
        # next 2C lines
        self.compiled_files = dict()

        for i in range(self.C):
            name, comp_time, repl_time = self.content[2 * i + 1].split()
            comp_time, repl_time = int(comp_time), int(repl_time) 
            compiled_file = CompiledFile(name, comp_time, repl_time)
            compiled_file.n_dependencies = int(self.content[2 * i + 2].split()[0])
            if compiled_file.n_dependencies > 0:
                compiled_file.dependencies = self.content[2 * i + 2].split()[1:]
            self.compiled_files[name] = compiled_file            

        # next T lines
        for i in range(T):
            name, deadline, goal_points = self.content[2 * C + 1 + i].split()
            self.compiled_files[name].TARGET_FILE = True
            self.compiled_files[name].DEADLINE = int(deadline)
            self.compiled_files[name].GOAL_POINTS = int(goal_points)

              
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

if __name__ == '__main__':
    args = arguments()
    if args.root[-1] != '/':
        args.root += '/'
    if args.path[-1] != '/':
        args.path += '/'
    dirname = args.root + args.path
    files = [
        dirname + fn for fn in os.listdir(dirname)
        if fn.endswith('.txt')]
    for fn in files:
        eg = Parser(fn)
        eg.parse()
        pickle.dump(eg, open(fn.replace('.txt', '.pkl'), 'wb'))
    
    eg.print_dir()
