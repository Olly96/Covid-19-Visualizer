import random

# def simulation_random_movement(population, infect_duration):
#         for i in population:
#             person = i.turtleObj
#             person.setx(person.xcor() + person.dx)
#             person.sety(person.ycor() + person.dy)
#             if (i.status == "I"):
#                 if (i.infected_time > infection_duration):
#                     print("infected time", i.infected_time)
#                     i.status = "R"
#                     person.color("gray")
from src import helpers

def get_displacement_coordinates(person, distance):
    print("laoasksa", person.x_limit)
    x = person.turtle.xcor()
    y = person.turtle.ycor()
    x_bound_1 = x - distance / 2
    x_bound_2 = x + distance / 2
    y_bound_1 = y - distance / 2
    y_bound_2 = y + distance / 2
    if x_bound_2 > person.x_limit[1]:
        x_bound_2 = person.x_limit[1]
    elif x_bound_1 < person.x_limit[0]:
        x_bound_1 = person.x_limit[0]
    if y_bound_2 > person.y_limit[1]:
        y_bound_2 = person.y_limit[1]
    elif y_bound_1 < person.y_limit[0]:
        y_bound_1 = person.y_limit[0]
    print("xbound_1", x_bound_1, "x_bound_2", x_bound_2, "y_bound_1", y_bound_1, "y_bound_2", y_bound_2)
    x_dest = random.uniform(x_bound_1, x_bound_2)
    y_dest = random.uniform(y_bound_1, y_bound_2)
    print("x_dest", x_dest)
    return [x_dest, y_dest]


def random_movement(person, config):
    person_turtle = person.turtle
    if random.random() < person.displacement_prob:
        if random.random() < config["sd_factor"]:
            disp_coordinates = get_displacement_coordinates(person, config["local_distance"])
            person_turtle.goto(disp_coordinates[0], disp_coordinates[1])
        else:
            disp_coordinates = get_displacement_coordinates(person, config["long_distance"])
            person_turtle.goto(disp_coordinates[0], disp_coordinates[1])


def simulate_random_movement(population, infected, recovered, config):
        for person_id in population.keys():
            person = population[person_id]
            person_turtle = person.turtle
            print("I am hete", person_id, person.displacement_prob)
            random_movement(person, config)
            update_infection_status(person, infected, recovered, config)




def update_infection_status(person, infected, recovered, config):
    person_turtle = person.turtle
    if person.is_ever_infected:
        person.infected_time += 1
    if person.status == "I" or person.status == "AI":
        if person.infected_time > config["infection_duration"]:
            person.status = "R"
            person_turtle.color("gray")
            recovered[person.id] = True
            del infected[person.id]
        else:
            if config["type"] == "SARS-COV-1":
                helpers.update_probability_sars(person, config)
            else:
                print("hello world")
                helpers.update_probability_covid(person, config)


def simulate_movement_communities(population, infected, recovered, config):
    for person_id in population.keys():
            person = population[person_id]
            person_turtle = person.turtle
            if random.random() < config["community_travel_probability"]:
                dest_community = random.choice(config["community_coordinates"])
                print(dest_community)
                x_dest = random.randint(dest_community[0], dest_community[1])
                y_dest = random.randint(dest_community[2], dest_community[3])
                person_turtle.goto(x_dest, y_dest)
            else:
                random_movement(person, config)

            update_infection_status(person, infected, recovered, config)


def simulate_movement_centralHub(population, infected, recovered, config):
    for person_id in population:
        person = population[person_id]
        person_turtle = person.turtle
        if(random.random() < config["visit_hub_probability"]):

            person.is_central_hub = True
            person_turtle.goto(random.randint(-20, 0), random.randint(-20, 0))
        else:
            if person.is_central_hub == True:
                disp_coordinates = get_displacement_coordinates(person, 50)
                print("foooooo", person.x_limit, person.y_limit, disp_coordinates)
                person.is_central_hub = False
                # x= random.choice([random.randint(100, 250), random.randint(-250, -100)])

                y = random.choice([random.randint(-250, -30), random.randint(30, 250)])

                person_turtle.goto(random.randint(-250, 250), y)
            else:
                random_movement(person, config)
        update_infection_status(person, infected, recovered, config)
