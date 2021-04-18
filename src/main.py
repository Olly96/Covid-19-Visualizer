import math
import turtle
import random
import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter import HORIZONTAL
import location
from src import screens, movement, helpers

# wn = turtle.Screen()
# wn.bgcolor('black')
# wn.title('Epidemic simulator')
# wn.tracer(0)
# foo = location.spawn_people_random(100, [-200, 200], [-200, 200])
# for person in foo:
#     print(person.id, person.turtle.xcor(), person.turtle.ycor())
# location.testFunc(population=foo)
# print(foo[2].status)
community_coordinates = [[-280, -100, 120, 300], [-80, 100, 120, 300], [120, 300, 120, 300], [-280, -100, -80, 100], [-80, 100, -80, 100], [120, 300, -80, 100], [-280, -100, -280, -100], [-80, 100, -280, -100], [120, 300, -280, -100]]
# foo = location.spawn_people_communities(100, community_coordinates)
# for person in foo:
#     print(person.id, person.turtle.xcor(), person.turtle.ycor())
# screens.create_random_mov_screen(start_coordinates=[-250, -250], side_length=500)
def garbage():
    draw_pen = turtle.Turtle()
    screens.create_central_hub_screen(draw_pen)
    draw_pen.clear()
    screens.create_communities_screen(draw_pen)
    # screens.create_quarantine_location([-300, -250], 40, draw_pen)
    screens.create_quarantine_location([-340, -300], 30, draw_pen)
    # print(len(foo))
    # movement.testFunc(population=foo)
    # print("hi",len(foo))

def social_dist(sd_factor, population):
    spaces_x = []
    spaces_y = []
    coordinates = []

    for i in range(-200, 201):
        if i % int(400 / math.sqrt(
                len(
                    population))) == 0:  # this is a calculation I created to make sure that more coordinates are created with a larger population
            # the weird population value, using the square of an odd number is part of this calculation.
            spaces_x.append(i)
            spaces_y.append(i)

    for x in spaces_x:
        for y in spaces_y:
            coordinate = [x, y]
            coordinates.append(coordinate)
    min_dist = 0
    closest_dist = []

    for i in range(len(population)):

        # if population[i].xcor() > -250:
            # this line above is only for quarantaine mode

            if random.randint(0, 100) in range(0, sd_factor + 1):

                for c in coordinates:

                    xdist = population[i].turtle.xcor() - c[0]
                    ydist = population[i].turtle.ycor() - c[1]
                    dist_squared = xdist * xdist + ydist * ydist
                    # dist_squared is the square of the distance to the coordinate in coordinates
                    if len(closest_dist) == 0:
                        closest_dist = c
                        min_dist = dist_squared
                    elif dist_squared < min_dist:
                        closest_dist = c
                        min_dist = dist_squared
                    # It looks for the closest coordinate in coordinates to the ball.

                if len(coordinates) > 0:
                    try:
                        coordinates.remove(closest_dist)
                        # this removes the coordinate that is already chosen by a ball from coordinates to make sure every coordinate gets only used once.
                    except:
                        coordinates.remove(coordinates[0])

                    # population[i].center_coordinates = [closest_dist[0], closest_dist[1]]
                    population[i].turtle.goto(closest_dist[0], closest_dist[1])

                closest_dist.clear()

foo =  True

def random_movement(canvas):
    sd_factor = 0.5
    config = {
        "infection_duration": 1440,
        "local_distance": 5,
        "long_distance": 30,
        "sd_factor": 0.6,
        "type": "SARS-COV-2",
        "infection_distance": 5,
        "mask_prob_infected_out_range": 0.2,
        "mask_prob_infected_in_range": 0.5,
        "mask_prob_susceptible": 0.5,
        "mask_prob_both_out_range": 0.02,
        "mask_prob_both_in_range": 0.25,
        "vaccine_probability": -1,
        "vaccine_efficacy_range": [0.64, 0.67, 0.94, 0.95],
        "mask_probability": -1,
        "time_conversion_factor": 24,
        "base_infection_probability": 0.6,
        "daily_prob_change": 0.9,
        "peak_infection_sars": 10,
        "daily_prob_increase_sars": 1.1,
        "daily_prob_decrease_sars": 0.9,
        "initial_infection_percentage": 2,
        "asymptomatic_probability": 0.3,
        "testing_probability": 0.5,
        "contact_tracing_efficiency": 1,
        "quarantine_location_x_limit": [-300, -260],
        "quarantine_location_y_limit": [-250, -210]
}
    susceptible = {}
    all_infections = {}
    victim_dict = {}
    infected = {}
    recovered = {}
    quarantined = {}
    close_contacts = {}
    final_R= []
    time = 0
    if config["type"] == "SARS-COV-1":
        incubation_period = random.randint(2, 7)
    else:
        incubation_period = 7
    population = location.spawn_people_random(225, [-200, 200], [-200, 200], incubation_period, canvas)
    iteration = 0
    for person_id in population.keys():
        population[person_id].displacement_prob = random.random()
        # population[person_id].is_infected = True
    social_dist(100, population)
    helpers.infect_random_people(population, config)
    helpers.filter_infectious(population, susceptible, infected)
    helpers.update_vaccination_and_mask_status(population, config)
    timesteps = 0
    while foo == True:
        time += 1
        timesteps += 1
        screen.update()
        # wn.update()
        quarantine_contacts = []
        # sd_factor
        movement.simulate_random_movement(population, infected, recovered, config)
        # if timesteps == config["time_conversion_factor"]:
        helpers.calculate_infections(population, susceptible, infected, config)
        susceptible = {}
        infected = {}
        helpers.filter_infectious(population, susceptible, infected)
            # timesteps = 0

        # iteration += 1
        # calculate_infections()
        # # print("infected length", len(infected))
        helpers.calculate_R(time, population, susceptible, all_infections, victim_dict, final_R, config)
        helpers.update_contacts(population, close_contacts, config)
        helpers.trace_contacts(population, infected, close_contacts, config)
        total_infec = 0
        # for key in all_infections.keys():
        #     total_infec += all_infections[key]
        # print("All infections lenght", total_infec)
        # index += 1

# def communities_movement():
#     config = {
#         "type": "SARS-COV-2",
#         "infection_distance": 5,
#         "mask_prob_infected_out_range": 0.2,
#         "mask_prob_infected_in_range": 0.5,
#         "mask_prob_susceptible": 0.5,
#         "mask_prob_both_out_range": 0.02,
#         "mask_prob_both_in_range": 0.25,
#         "vaccine_probability": -1,
#         "vaccine_efficacy_range": [0.64, 0.67, 0.94, 0.95],
#         "mask_probability": -1,
#         "time_conversion_factor": 24,
#         "base_infection_probability": 0.6,
#         "daily_prob_change": 0.9,
#         "peak_infection_sars": 10,
#         "daily_prob_increase_sars": 1.1,
#         "daily_prob_decrease_sars": 0.9,
#         "initial_infection_percentage": 2,
#         "asymptomatic_probability": 0.3,
#         "testing_probability": 0.5,
#         "contact_tracing_efficiency": 1,
#         "quarantine_location_x_limit": [-300, -260],
#         "quarantine_location_y_limit": [-250, -210],
#         "community_travel_probability": 0.02,
#         "visit_hub_probability": 0.1,
#         "community_coordinates": [[-280, -100, 120, 300], [-80, 100, 120, 300], [120, 300, 120, 300], [-280, -100, -80, 100], [-80, 100, -80, 100], [120, 300, -80, 100], [-280, -100, -280, -100], [-80, 100, -280, -100], [120, 300, -280, -100]],
#         "sd_factor": 0.7
# }
#     susceptible = {}
#     all_infections = {}
#     victim_dict = {}
#     infected = {}
#     recovered = {}
#     quarantined = {}
#     close_contacts = {}
#     final_R= []
#     time = 0
#     if config["type"] == "SARS-COV-1":
#         incubation_period = random.randint(2, 7)
#     else:
#         incubation_period = 7
#     population = location.spawn_people_communities(225, config["community_coordinates"], incubation_period)
#     iteration = 0
#     for person_id in population.keys():
#         population[person_id].displacement_prob = 1
#         # population[person_id].is_infected = True
#     social_dist(100, population)
#     helpers.infect_random_people(population, config)
#     helpers.filter_infectious(population, susceptible, infected)
#     helpers.update_vaccination_and_mask_status(population, config)
#     timesteps = 0
#     while True:
#         time += 1
#         timesteps += 1
#         quarantine_contacts = []
#         # sd_factor
#         movement.simulate_movement_communities(population, config)
#         wn.update()
#         # if timesteps == config["time_conversion_factor"]:
#         # helpers.calculate_infections(population, susceptible, infected, config)
#         # susceptible = {}
#         # infected = {}
#         # helpers.filter_infectious(population, susceptible, infected)
#             # timesteps = 0
#
#         # iteration += 1
#         # calculate_infections()
#         # # print("infected length", len(infected))
#         # helpers.calculate_R(time, population, susceptible, all_infections, victim_dict, final_R, config)
#         # helpers.update_contacts(population, close_contacts, config)
#         # helpers.trace_contacts(population, infected, close_contacts, config)
#         total_infec = 0
#         # for key in all_infections.keys():
#         #     total_infec += all_infections[key]
#         # print("All infections lenght", total_infec)
#         # index += 1


# def central_hub_movement():
#     # screens.create_random_mov_screen()
#
#     draw_pen = turtle.Turtle()
#     screens.create_central_hub_screen(draw_pen)
#     config = {
#         "type": "SARS-COV-2",
#         "infection_duration": 1440,
#         "infection_distance": 5,
#         "mask_prob_infected_out_range": 0.2,
#         "mask_prob_infected_in_range": 0.5,
#         "mask_prob_susceptible": 0.5,
#         "mask_prob_both_out_range": 0.02,
#         "mask_prob_both_in_range": 0.25,
#         "vaccine_probability": -1,
#         "vaccine_efficacy_range": [0.64, 0.67, 0.94, 0.95],
#         "mask_probability": -1,
#         "time_conversion_factor": 24,
#         "base_infection_probability": 0.6,
#         "daily_prob_change": 0.9,
#         "peak_infection_sars": 10,
#         "daily_prob_increase_sars": 1.1,
#         "daily_prob_decrease_sars": 0.9,
#         "initial_infection_percentage": 2,
#         "asymptomatic_probability": 0.3,
#         "testing_probability": 0.5,
#         "contact_tracing_efficiency": 1,
#         "quarantine_location_x_limit": [-300, -260],
#         "quarantine_location_y_limit": [-250, -210],
#         "community_travel_probability": 0.02,
#         "visit_hub_probability": 0.01,
#         "community_coordinates": [[-280, -100, 120, 300], [-80, 100, 120, 300], [120, 300, 120, 300], [-280, -100, -80, 100], [-80, 100, -80, 100], [120, 300, -80, 100], [-280, -100, -280, -100], [-80, 100, -280, -100], [120, 300, -280, -100]],
#         "sd_factor": 0.8
# }
#     susceptible = {}
#     all_infections = {}
#     victim_dict = {}
#     infected = {}
#     recovered = {}
#     quarantined = {}
#     close_contacts = {}
#     final_R= []
#     time = 0
#     if config["type"] == "SARS-COV-1":
#         incubation_period = random.randint(2, 7)
#     else:
#         incubation_period = 7
#     population = location.spawn_people_random(225, [-250, 250],[-250, 250], incubation_period)
#     iteration = 0
#     for person_id in population.keys():
#         population[person_id].displacement_prob = 1
#         # population[person_id].is_infected = True
#     social_dist(100, population)
#     helpers.infect_random_people(population, config)
#     helpers.filter_infectious(population, susceptible, infected)
#     helpers.update_vaccination_and_mask_status(population, config)
#     timesteps = 0
#     while True:
#         time += 1
#         timesteps += 1
#         quarantine_contacts = []
#         # sd_factor
#         movement.simulate_movement_centralHub(population, config)
#         wn.update()
#         # if timesteps == config["time_conversion_factor"]:
#         # helpers.calculate_infections(population, susceptible, infected, config)
#         # susceptible = {}
#         # infected = {}
#         # helpers.filter_infectious(population, susceptible, infected)
#             # timesteps = 0
#
#         # iteration += 1
#         # calculate_infections()
#         # # print("infected length", len(infected))
#         # helpers.calculate_R(time, population, susceptible, all_infections, victim_dict, final_R, config)
#         # helpers.update_contacts(population, close_contacts, config)
#         # helpers.trace_contacts(population, infected, close_contacts, config)
#         total_infec = 0
#         # for key in all_infections.keys():
#         #     total_infec += all_infections[key]
#         # print("All infections lenght", total_infec)
#         # index += 1
def on_field_change(index, value, op):
    # print("combobox updated to ", c.get())
    random_movement(0.5)

    #print("Slider updated to ", w2.get())

# def on_slider_change(index, value, op):
#     #print("combobox updated to ", c.get())
#     print("Slider updated to ", w2.get())
root = tk.Tk()
root.geometry('1500x1500')

canvas = tk.Canvas(master = root, width = 700, height = 800)

# canvas = turtle.ScrolledCanvas(root)
# canvas.place(x=300, y=300)
canvas.pack(side=tk.RIGHT)
screen = turtle.TurtleScreen(canvas)
screen.bgcolor('black')
# screen.title('Epidemic simulator')
screen.tracer(0)
# screen.tracer(0)
canvas.pack()
def btnClicked():
    global  foo
    foo = False
    print("event")

def print_value(val):
    print(scale.get())

btn = tk.Button(master = root, bg="white", fg="black",text = "Forward", command = btnClicked)
scale = tk.Scale(orient='horizontal', from_=0, to=128)
scale.bind("<ButtonRelease-1>", print_value)
scale.place(x=40, y=70)
btn.place(x=10, y=20)
# ttk.Label(root, text = "Select a virus :",
#         font = ( 10)).grid(column = 0,
#         row = 15, padx = 10, pady = 25)
# v = tk.StringVar()
# v.trace('w',on_field_change)
# c = ttk.Combobox(root, textvar=v, state="readonly", values=["SARS-CoV", "SARS-CoV-2"])
# c.pack()
# c.grid(column = 1, row = 25)
random_movement(screen)
# central_hub_movement()
root.mainloop()
