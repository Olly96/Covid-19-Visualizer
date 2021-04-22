import random
from src import person
from src import constants
def spawn_people_random(config, x_limit, y_limit, canvas):
    population = {}
    for i in range(config[constants.population]):
        person_obj = person.Person(i, x_limit, y_limit, config[constants.incubation_period], config[constants.particle_size],  canvas)
        person_obj.vaccine_efficacy = config[constants.vaccine_efficacy]
        population[i] = person_obj
    return population


def spawn_people_communities(config,  canvas):
    population = {}
    for i in range(len(config[constants.community_coordinates])):
        population_count = int((1/len(config[constants.community_coordinates])) * config[constants.population])
        for j in range(population_count):
            x_limit = [config[constants.community_coordinates][i][0], config[constants.community_coordinates][i][1]]
            y_limit = [config[constants.community_coordinates][i][2], config[constants.community_coordinates][i][3]]
            person_obj = person.Person(j + i*population_count, x_limit, y_limit, config[constants.incubation_period], config[constants.particle_size],  canvas)
            person_obj.vaccine_efficacy = config[constants.vaccine_efficacy]
            population[j + i*population_count] = person_obj
    return population

