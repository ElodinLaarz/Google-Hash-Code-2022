import argparse
import inspect
import os
import pickle

def arguments():
    parser = argparse.ArgumentParser(description='Get(s) the path to input files')
    parser.add_argument('--root', '-r', type=str, default=None)
    parser.add_argument('--path', '-p', type=str, default=None)
    return parser.parse_args()

class GoogleLibrary:
    def __init__(self, n_books, n_days, n_scans, books_ids, books_scores):
        self.n_books = n_books
        self.N = self.n_books
        self.n_days = n_days
        self.T = self.n_days
        self.n_scans = n_scans
        self.M = self.n_scans
        self.finish_scaning = False
        # sorting books
        books_ids.sort(key = lambda book: books_scores[book], reverse=True)
        self.books_ids = books_ids
        self.total_score = 0
        self.max_book_score = 0
        for book in self.books_ids:
            self.total_score += books_scores[book]
            self.max_book_score = max([self.max_book_score, books_scores[book]])
    
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
        # settings
        content = [int(ele) for ele in self.content[0].split()]
        self.n_books = content[0]
        self.B = content[0]
        self.n_libraries = content[1]
        self.L = content[1]
        self.n_days = content[2]
        self.D = content[2]
        
        # score of individual books.
        books_scores = [int(ele) for ele in self.content[1].split()] 
        self.book_scores = dict()
        for book, score in enumerate(books_scores):
            self.book_scores[book] = score

        # next 2L lines: Library description
        self.libraries = []
        for i in range(self.L):
            lines_number = [2 + 2*i, 2 + 2*i + 1]
            info = [int(ele) for ele in self.content[lines_number[0]].split()]
            books_ids = [int(ele) for ele in self.content[lines_number[1]].split()]
            this_library = GoogleLibrary(info[0], info[1], info[2], books_ids, self.book_scores)
            setattr(this_library, 'id', i)
            self.libraries.append(this_library)


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
