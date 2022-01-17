import numpy as np
import random


def scoring(people_dict, ingredient_list):
    score = []
    for person in people_dict:
        likes = people_dict[person]['likes']
        dislikes = people_dict[person]['dislikes']
        if (
            len([l for l in likes if l in ingredient_list]) == len(likes) and
            len([d for d in dislikes if d not in ingredient_list]) == len(dislikes)
        ):
            score.append(person)
    return len(score)


best_pizza = []
best_pizza_score = 0

file_names = ['a', 'b', 'c', 'd', 'e']

for file_name in file_names:

    for _ in range(1):
        A = open(f'./input/{file_name}.in', 'r').readlines()
        n_people = int(A[0].strip())
        people_dict = dict()
        ingredients_dict = dict()
        for i in range(n_people):
            like_row = A[2*i + 1]
            dislike_row = A[2*i + 2]
            n_likes = int(like_row.split()[0])
            likes = set(like_row.split()[1:])
            n_dislikes = int(dislike_row.split()[0])
            dislikes = set(dislike_row.split()[1:])
            people_dict[i] = {
                'n_likes': n_likes,
                'likes': likes,
                'n_dislikes': n_dislikes,
                'dislikes': dislikes        
            }
            for l in likes:
                if l in ingredients_dict:
                    ingredients_dict[l]['likes'].add(i)
                else:
                    ingredients_dict[l] = {'likes': set(), 'dislikes': set()}
                    ingredients_dict[l]['likes'].add(i) 
            for d in dislikes:
                if d in ingredients_dict:
                    ingredients_dict[d]['dislikes'].add(i)
                else:
                    ingredients_dict[d] = {'likes': set(), 'dislikes': set()}
                    ingredients_dict[d]['dislikes'].add(i)

        # Get keys with conflicts:

        conflicts = []

        for ingredient in ingredients_dict:
            if ingredients_dict[ingredient]['likes'] and ingredients_dict[ingredient]['dislikes']:
                conflicts.append(ingredient)

        conflicts.sort(key=lambda x: min(len(ingredients_dict[x]['likes']),len(ingredients_dict[x]['dislikes'])))
        # for conflict in conflicts: 
        #     print(conflict, min(len(ingredients_dict[conflict]['likes']),len(ingredients_dict[conflict]['dislikes'])))
        # print(ingredients_dict)
        while (conflicts):
            weights = np.array([x+1 for x in range(len(conflicts))])
            norm = sum(weights)
            weights = weights/norm
            weights = [int(x*1000)/1000 for x in weights]
            weights[-1] = 1-sum(weights[:-1])

            ingredient = np.random.choice(conflicts, 1, p = weights)[0]

            if(ingredients_dict[ingredient]['likes'] and ingredients_dict[ingredient]['dislikes']):
    #             coin_flip = random.randint(0,1)

                if len(ingredients_dict[ingredient]['likes']) < len(ingredients_dict[ingredient]['dislikes']):
                    person_to_remove = next(iter(ingredients_dict[ingredient]['likes']))
                else:
                    person_to_remove = next(iter(ingredients_dict[ingredient]['dislikes']))
                likes = people_dict[person_to_remove]['likes']
                dislikes = people_dict[person_to_remove]['dislikes']
            #     print(likes)
                for like in likes:
                    ingredients_dict[like]['likes'].remove(person_to_remove)
            #     print(dislikes)
            #     print(ingredients_dict)
                for dislike in dislikes:
                    ingredients_dict[dislike]['dislikes'].remove(person_to_remove)
            else:
                conflicts.remove(ingredient)

        pizza = []

        for ingredient in ingredients_dict:
            if ingredients_dict[ingredient]['likes']:
                pizza.append(ingredient)
        if not best_pizza:
            best_pizza = pizza
            best_pizza_score = scoring(people_dict, pizza)
        else:
            score = scoring(people_dict, pizza)
            if score > best_pizza_score:
                best_pizza = pizza
                best_pizza_score = score
                
    with open(f'./output/{file_name}.out', 'w') as f:
        f.write(str(len(best_pizza)) + " " + " ".join(best_pizza))

#     print(best_pizza_score)