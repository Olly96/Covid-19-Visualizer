import random
from src import person

def spawn_people_random(count, x_limit, y_limit, incubation_period, canvas):
    population = {}
    for i in range(count):
        person_obj = person.Person(i, x_limit, y_limit, incubation_period, canvas)
        population[i] = person_obj
    return population


def spawn_people_communities(count, community_coordinates, incubation_period, canvas):
    population = {}
    for i in range(len(community_coordinates)):
        population_count = int((1/len(community_coordinates)) * count)
        for j in range(population_count):
            x_limit = [community_coordinates[i][0], community_coordinates[i][1]]
            y_limit = [community_coordinates[i][2], community_coordinates[i][3]]
            person_obj = person.Person(j + i*population_count, x_limit, y_limit, incubation_period, canvas)
            population[i] = person_obj
    return population

