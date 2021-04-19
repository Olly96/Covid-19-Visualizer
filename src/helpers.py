import random

def calculate_R(time, population, susceptible, infected_dict, victim_dict, final_R, config):
    if (time/config["time_conversion_factor"]) % 7 == 0 and len(susceptible.keys()) > 0:
        # print("t/12", time/config["time_conversion_factor"])
        print("t/12", time/config["time_conversion_factor"])
        x = []
        y = []
        # graph_days = time/24 - 1
        # total_days = time/24
        graph_days = time/config["time_conversion_factor"] - 1
        total_days = time/config["time_conversion_factor"]
        interval = 7
        win_size = 28
        for person_id in population.keys():
            person = population[person_id]
            if person.is_ever_infected and person.id not in victim_dict.keys():
                # print(person.status)
                if person.infected_by in infected_dict.keys():
                    infected_dict[person.infected_by] += 1
                elif person.infected_by != "None":
                    infected_dict[person.infected_by] = 1
                victim_dict[person.id] = True
        start_day = 7
        win_right = start_day
        while(win_right <= total_days):
            win_left = max(win_right-win_size, 0)
            x.append(win_right)
            total_infections = 0
            total_edges = 0
            for local_person_id in population.keys():
                person = population[local_person_id]
                if person.is_ever_infected:
                    when_infected = total_days - person.infected_time/config["time_conversion_factor"]
                            # when_infected = total_days - person.infected_time
                            # when_infected = person.infected_timestamp / 24
                    if when_infected >= win_left and when_infected < win_right:
                        total_infections += 1
                        if person.id in infected_dict.keys():
                            total_edges += infected_dict[person.id]
            if total_infections == 0:
                y.append(0)
            else:
                y.append(total_edges/total_infections)
            win_right += interval
        print(x, y)
        # if(len(y)>0):
        #     final_R.append(y[len(y)-1])
        #     print(final_R)


        # for key in infected_dict.keys():
        #     total_edges += infected_dict[key]
        # if len(infected_dict.keys()) != 0:
        #     print("Infected", total_infections, " ", total_edges/len(infected_dict.keys()))
        #     return total_edges/len(infected_dict.keys())
        # else:
        #     return 0


def filter_infectious(population, susceptible, infected):
    for person_id in population.keys():
        person_status = population[person_id].status
        if person_status == "S":
            susceptible[person_id] = True
        elif person_status == "I" or person_status == "AI":
            infected[person_id] = True

def update_contacts(population, contacts, config):
    for person_id in population.keys():
        person_1 = population[person_id]
        turtle_1 = person_1.turtle
        if person_1.status == "I" or person_1.status == "AI":
            for person_2_id in population.keys():
                person_2 = population[person_2_id]
                if person_2_id != person_id:
                    turtle_2 = person_2.turtle
                    if turtle_1.distance(turtle_2) <= config["infection_distance"] and \
                            random.random() < config["contact_tracing_efficiency"]:
                        if person_id in contacts:
                            contacts[person_id][person_2_id] = True
                        else:
                            contacts[person_id] = {person_2_id: True}


def trace_contacts(population, infected, contacts, config):
    for infected_person_id in infected.keys():
        infected_person = population[infected_person_id]
        if infected_person_id in contacts:
            if infected_person.status == "I" or \
                (infected_person.status == "AI" and
                 random.random() < config["asymptotic_testing_probability"]):
                if infected_person.infected_time > infected_person.incubation_period * config["time_conversion_factor"]:
                    quarantine_person(infected_person, config)
                    for contact_id in contacts[infected_person_id].keys():
                        contact = population[contact_id]
                        if contact.infected_time > contact.incubation_period * config["time_conversion_factor"]\
                                or random.random() < config["quarantine_probability"]:
                            quarantine_person(contact, config)
                    # del contacts[infected_person_id]


def quarantine_person(person, config):
    if person.status == "I" or person.status == "AI":
        person.status = "QI"
    else:
        person.status = "QS"
    x = random.randint(config["quarantine_location_x_limit"][0],
                       config["quarantine_location_x_limit"][1])
    y = random.randint(config["quarantine_location_y_limit"][0],
                       config["quarantine_location_y_limit"][1])
    person.turtle.goto(x, y)
    person.x_limit = config["quarantine_location_x_limit"]
    person.y_limit = config["quarantine_location_y_limit"]
    person.is_quarantined = True

def infect_random_people(population, config):
    population_keys = []
    for key in population.keys():
        population_keys.append(key)
    population_keys_length = len(population_keys)
    for i in range(int(config["initial_infection_percentage"]/100 * len(population))):
        index = random.randint(0, population_keys_length-1)
        person_id = population_keys[index]
        population[person_id].displacement_prob = 1
        population[person_id].turtle.color("red")
        population[person_id].is_ever_infected = True
        if random.random() < config["asymptomatic_probability"]:
            population[person_id].status = "AI"
        else:
            population[person_id].status = "I"


def update_probability_sars(infected, config):
    infected.update_prob_tracker += 1
    if infected.infection_probability == 0:
        if infected.infected_time >= infected.incubation_period * config["time_conversion_factor"]:
            infected.infection_probability = config["base_infection_probability"]
            infected.update_prob_tracker = 0

    elif infected.update_prob_tracker >= config["time_conversion_factor"]:
        if infected.infected_time > config["peak_infection_sars"] * config["time_conversion_factor"]:
            infected.infection_probability = config["daily_prob_decrease_sars"] * infected.infection_probability
        else:
            infected.infection_probability = config["daily_prob_increase_sars"] * infected.infection_probability
        infected.update_prob_tracker = 0

def update_probability_covid(infected, config):
    infected.update_prob_tracker += 1
    if infected.infection_probability == 0:
        if infected.infected_time >= max((infected.incubation_period - 3), 0) * config["time_conversion_factor"]:
            infected.infection_probability = config["base_infection_probability"]
            infected.turtle.color("red")
            infected.update_prob_tracker = 0

    elif infected.update_prob_tracker >= config["time_conversion_factor"]:
        infected.infection_probability = config["daily_prob_change"] * infected.infection_probability
        infected.update_prob_tracker = 0

    # print("infected infectionprob", infected.infection_probability)

def update_vaccination_and_mask_status(population, config ):
    for person_id in population.keys():
        if random.random() < config["vaccine_probability"]:
            # print("vaccine probabilit True")
            population[person_id].vaccination_status = True
            population[person_id].vaccine_efficacy = random.choice(config["vaccine_efficacy_range"])
        if random.random() < config["mask_probability"]:
            # print("mask probability")
            population[person_id].mask_status = True

def get_effective_probability(infected_person, susceptible_person, distance, config):
    effective_probability = infected_person.infection_probability
    if susceptible_person.vaccination_status:
        effective_probability *= 1 - susceptible_person.vaccine_efficacy

    if infected_person.mask_status and not susceptible_person.mask_status:
        if distance > config["infection_distance"]/2:
            effective_probability *= config["mask_prob_infected_out_range"]
        else:
            effective_probability *= config["mask_prob_infected_in_range"]
    elif not infected_person.mask_status and susceptible_person.mask_status:
        effective_probability *= config["mask_prob_susceptible"]
    elif infected_person.mask_status and susceptible_person.mask_status:
        if distance > config["infection_distance"]/2:
            effective_probability *= config["mask_prob_both_out_range"]
        else:
            effective_probability *= config["mask_prob_both_in_range"]
    return effective_probability


def get_infection_status(infected_person, susceptible_person, config):
    distance = susceptible_person.turtle.distance(infected_person.turtle)
    infection_status = False
    if distance < config["infection_distance"]:
        effective_probability = get_effective_probability(infected_person, susceptible_person, distance, config)
        if random.random() < effective_probability:
            infection_status = True
    return infection_status


def calculate_infections(population, susceptible, infected, config):
    for susceptible_id in susceptible.keys():
        for infected_id in infected.keys():
            # x_dist = abs(susceptible[i].turtleObj.xcor() - infected_per.turtleObj.xcor())
            # y_dist = abs(susceptible[i].turtleObj.ycor() - j.turtleObj.ycor())
            # dist_squared = x_dist * x_dist + y_dist * y_dist
            # if config["type == "SARS-COV-1":
            infection_status = get_infection_status(population[infected_id], population[susceptible_id], config)
            if infection_status:
                susceptible_person = population[susceptible_id]
                susceptible_person.turtle.color("yellow")
                susceptible_person.infected_by = infected_id
                susceptible_person.is_ever_infected = True
                if random.random() < config["asymptomatic_probability"]:
                    susceptible_person.status = "AI"
                else:
                    susceptible_person.status = "I"
                break
            # else:
            #     infection_status = get
    # print("inf_count:", inf_count)

    # for i in range(len(susceptible)):
    #     if i not in delete_indexes:
    #         new_pop.append(susceptible[i])
    #     else:
    #         infected.append(susceptible[i])
    # susceptible = new_pop

    # display_string = "Infected:" + str(len(infected))
    # foo.clear()
    # foo.goto(0, 300)
    # foo.write(display_string, True, align="center", font=("Arial", 25, "normal"))
    # foo.hideturtle()
