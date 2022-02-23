from simulation import Simulator
from parser import Parser
# from sloth_scorer import Score


if __name__ == '__main__':
    file_prefixes = ['a', 'b', 'c', 'd', 'e']

    total_score = 0

    for prefix in file_prefixes:
        p = Parser('./inputs/' + prefix + '.in')
        # p.parse()

        current_simulation = Simulator(p.data(), prefix)

    while (current_simulation.time_remaining > 0):
        current_simulation.time_step()

        current_simulation.create_output()

        cur_score = Score('./outputs/' + prefix + '.out')

        prev_score = 0
    with open('./scores/' + prefix + '.score', 'r') as f:
        prev_score = int(f.readline().strip())

        better_score = max(cur_score, prev_score)

        total_score += better_score

        print(f'You scored {cur_score} on {prefix}.')
        if(cur_score > prev_score):
          # TODO: Copy output file into a new 'best' location
          print('This is a better score! A new best output file has been noted.')
        else:
            print('This score was not an improvement.')

        print(f'Your sum of best scores is now {total_score}')
