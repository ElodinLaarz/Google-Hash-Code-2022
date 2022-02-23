import argparse
import inspect
import os
import pickle

def arguments():
    parser = argparse.ArgumentParser(description='Get(s) the path to input files')
    parser.add_argument('--root', '-r', type=str, default=None)
    parser.add_argument('--path', '-p', type=str, default=None)
    return parser.parse_args()

class AuxiliaryClass:
    def __init__(self, att1, att2):
        self.att1 = att1
        self.att2 = att2
    
    def additional_function(self):
        pass

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
        
    def parse(self):
        # line one content
        content = [int(ele) for ele in self.content[0].split()]
        self.att_name0 = content[0]
        self.att_var0 = content[0]
        self.att_name1 = content[1]
        self.att_var1 = content[1]       
        # next A lines
        self.att_name = [] # or dict() or tuple()
        for i in range(1, 1 + self.A):
       
        # next B lines
        self.att_name = []
        for i in range(1 + self.A, 1 + self.A + self.B):
        
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
