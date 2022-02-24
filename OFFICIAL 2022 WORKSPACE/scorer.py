from dataclasses import dataclass
import itertools as it
from parser_books import Parser

@dataclass
class LibrarySubmission:
    library: int
    books_sent: int
    books: list

    def signup_time(self, A) -> int:
        return A.libraries[self.library].T

    def books_per_day(self, A) -> int:
        return A.libraries[self.library].M
    
    def book_scores(self, A) -> list:
        return map(lambda x: A.book_scores[x], self.books)

class Scorer:
    def __init__(self, input_file='', output_file=''):
        self.input = input_file
        self.output = output_file
        self.A = Parser(self.input)
        self.A.parse()
    
    def ScoreLibrary(self, lib, days_remaining=0):
        days_remaining = days_remaining - lib.signup_time(self.A)
        book_scores = lib.book_scores(self.A)
        bpd = lib.books_per_day(self.A)
        score = 0
        for days in range(days_remaining):
            score += sum(it.islice(book_scores, bpd))
        return score
    
    def score(self):
        with open(self.output,'r') as fp:
            data = [x.strip() for x in fp.readlines() if x]
        num_libraries = int(data.pop(0))
        submission = []
        seen = set()
        for i in range(0, len(data), 2):
            library, books_sent = *map(int,data[i].split(' ')),
            if books_sent > 0 and not library in seen:
                seen.add(library)
                books = list(map(int, data[i+1].split(' ')))
               # print(sorted(books), sorted(list(set(books))))
                if sorted(books) != sorted(list(set(books))):
                    raise ValueError(f'Duplicate books in library {library}')
                submission.append(LibrarySubmission(library, books_sent, books))
        
        dr = self.A.D
        score = 0
        for library in submission:
            score += self.ScoreLibrary(library, days_remaining=dr)
            dr -= library.signup_time(self.A)
        return score