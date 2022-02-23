import shutil

from simulation import Simulator
from F2019.parser import Parser
# from sloth_scorer import Score


if __name__ == '__main__':
    # file_prefixes = ['a', 'b', 'c', 'd', 'e']
    file_prefixes = ['a']

    total_score = 0

    for prefix in file_prefixes:
        p = Parser('./inputs/' + prefix + '.in')

        current_simulation = Simulator(p.data(), prefix)

    while (current_simulation.time_remaining > 0):
        current_simulation.time_step()

    current_simulation.create_output()

    cur_score = Score('./outputs/' + prefix + '.out')

    total_score = 0
    with open('./scores/' + prefix + '.score', 'r') as f:
        prev_score = int(f.readline().strip())

        better_score = max(cur_score, prev_score)

        total_score += better_score

        print(f'You scored {cur_score} on {prefix}.')
        if(cur_score > prev_score):
            shutil.copy('./outputs/'+prefix+'.out', './best_outputs/')
            with open('./scores/' + prefix + '.score', 'w') as g:
                g.write(str(better_score))
            print('This is a better score! A new best output file has been noted.')
        else:
            print('This score was not an improvement.')

    print(f'Your sum of best scores is now {total_score}')
