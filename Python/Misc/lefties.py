import random
import time

SINGLE = 0
MARRIED = 1
DEAD = 2


initial_population_size = 100
simulation_years = 200

maximal_age = 60

minimal_marriage_age = 18
maximal_marriage_difference = 10

minimal_reproduction_age = 18
maximal_reproduction_age = 45
maximal_offspring = 2
reproduction_probability = 0.1


def _is_couple_marriable(human1, human2):
    return abs(human1['age'] - human2['age']) <= maximal_marriage_difference


def _is_human_marriable(human):
    return human['age'] >= minimal_marriage_age and human['status'] == SINGLE


def _can_have_children(couple):
    hid1 = couple['human_ids'][0]
    human1 = population[hid1]

    hid2 = couple['human_ids'][1]
    human2 = population[hid2]

    if human1['age'] > maximal_reproduction_age or human1['age'] < minimal_reproduction_age or human1['status'] == 'dead':
        return False

    if human2['age'] > maximal_reproduction_age or human2['age'] < minimal_reproduction_age or human2['status'] == 'dead':
        return False

    if couple['num_offspring'] == maximal_offspring:
        return False

    return True


def _randomize_leftiness(couple=None):
    if couple is None:
        return random.random() < 0.5

    hid1 = couple['human_ids'][0]
    leftie1 = population[hid1]['leftie']

    hid2 = couple['human_ids'][1]
    leftie2 = population[hid2]['leftie']

    if leftie1 and leftie2:
        return random.random() < 0.46
    if leftie1 or leftie2:
        return random.random() < 0.17
    return random.random() < 0.02

newborn = list()
population = list()
dead = list()

couples = list()
human_id_counter = 0
human_counter = 0
for i in range(0, initial_population_size):
    human = {'id': human_id_counter, 'age': 0, 'status': SINGLE, 'leftie': _randomize_leftiness()}
    newborn.append(human)
    human_counter += 1
    human_id_counter += 1

year = 0
for year in range(0, simulation_years):
    if year > minimal_marriage_age:
        time.sleep(0.5)
    year += 1

    for human in population:
        human['age'] += 1
        if human['age'] > maximal_age:
            human['status'] = DEAD
            human_counter -= 1

    for human in newborn:
        newborn['age'] += 1
        if newborn['age'] >= minimal_marriage_age:
            newborn.remove(human)
            population.append(human)

    legal_singles = [human['id'] for human in population if _is_human_marriable(human)]
    while len(legal_singles) > 1:
        humans = random.sample(legal_singles, 2)
        couple = {'human_ids': humans, 'num_offspring': 0}
        couples.append(couple)

        legal_singles.remove(humans[0])
        legal_singles.remove(humans[1])

    for couple in couples:
        if not _can_have_children(couple):
            continue

        if random.random() < reproduction_probability:
            population.append({'id': human_id_counter, 'age': 0, 'status': SINGLE, 'leftie': _randomize_leftiness(couple)})
            human_id_counter += 1
            human_counter += 1

    num_lefties = sum(1 for human in population if human['leftie'] and not human['status'] == DEAD)
    mean_age = sum(human['age'] for human in population) / human_counter

    print 'Year: %d, Size: %d, Average Age: %f, Lefties: %f' % (year, human_id_counter, mean_age, float(num_lefties) / human_counter * 100)





