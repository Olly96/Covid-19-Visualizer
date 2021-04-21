import math
import turtle
import random
import tkinter as tk
from tkinter import *
from src import location
from src import screens, movement, helpers
from configparser import ConfigParser
from src import constants
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg,NavigationToolbar2Tk)
root = tk.Tk()
parser = ConfigParser()
GUI_CONFIG_PARAMS = {}
UI_ELEMENTS_MAP = {}
run_simulation = True


parser.read('mydev.ini')
population_percentage = {
    'line1' : [228, 284, 365, 631, 477, 814, 1044, 1275],
    'line2' : [228, 365, 631, 284, 814, 1044, 477, 1275],
    'line3' : [228, 631, 814, 1044, 284, 477, 365, 1275]
}
time_list = [10, 20, 30, 40, 50, 60, 70, 80]
r_factor = [3, 5, 1, 7, 10]

def make_stackplot(stack_percentage_obj, tl):
    fig, ax = plt.subplots(figsize=(3.9, 3.9))
    ax.stackplot(tl, stack_percentage_obj.values(),
                 labels=stack_percentage_obj.keys())
    plot = ax
    ax.legend(loc='upper left')
    ax.set_title('Covid-19 Visualizer')
    ax.set_xlabel('Time')
    ax.set_ylabel('Population')
    fig.tight_layout()
    canvas_stackplot = FigureCanvasTkAgg(fig,
                                         master=root)
    canvas_stackplot.get_tk_widget().grid(row=0, column=0, padx=(0, 0), pady=(0, 0))


def make_lineplot(time, r_values):
    print(time, r_values)
    fig, ax = plt.subplots(figsize=(3.9, 3.9))
    ax.plot(time, r_values)
    #ax.legend(loc='upper left')
    ax.set_title('R-Factor')
    ax.set_xlabel('X-Axis Title')
    ax.set_ylabel('Y-Axis Title')
    fig.tight_layout()
    canvas_lineplot = FigureCanvasTkAgg(fig,
                                         master=root)
    canvas_lineplot.draw()

    # placing the canvas on the Tkinter window
    #canvas_lineplot.get_tk_widget().pack(side=tk.LEFT, fill=tk.X)
    canvas_lineplot.get_tk_widget().grid(row=0, column=1, padx=(0, 0), pady=(0, 0))

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


def update_graphs(population_percentage, time_list, population_len, susceptible_len,
                  infected_len, recovered_len, time,  r_vals):
    population_percentage['susceptible'].append(susceptible_len * 100 / population_len)
    population_percentage['infected'].append(infected_len * 100 / population_len)
    population_percentage['recovered'].append(recovered_len * 100 / population_len)
    time_list.append(time)
    plt.cla()
    make_stackplot(population_percentage, time_list)
    make_lineplot(r_vals[0], r_vals[1])


def random_movement(canvas, config):
    susceptible = {}
    all_infections = {}
    victim_dict = {}
    infected = {}
    recovered = {}
    quarantined = {}
    close_contacts = {}
    final_R= []
    time = 0
    population_percentage = {
        'infected': [],
        'susceptible': [],
        'recovered': []
    }
    time_list = []
    r_vals = [[], []]
    make_stackplot(population_percentage, time_list)
    make_lineplot(r_vals[0], r_vals[1])
    population = location.spawn_people_random(225, [-200, 200], [-200, 200], config["incubation_period"], canvas)
    iteration = 0
    for person_id in population.keys():
        population[person_id].displacement_prob = random.random()
        # population[person_id].is_infected = True
    social_dist(100, population)
    helpers.infect_random_people(population, config)
    helpers.filter_infectious(population, susceptible, infected)
    helpers.update_vaccination_and_mask_status(population, config)
    timesteps = 0
    while run_simulation == True:
        time += 1
        timesteps += 1
        canvas.update()
        movement.simulate_random_movement(population, infected, recovered, config)
        helpers.calculate_infections(population, susceptible, infected, config)
        susceptible = {}
        infected = {}
        helpers.filter_infectious(population, susceptible, infected)
        r_vals = helpers.calculate_R(time, population, susceptible, all_infections, victim_dict, config, r_vals)
        helpers.update_contacts(population, close_contacts, config)
        # helpers.trace_contacts(population, infected, close_contacts, config)
        counts = helpers.get_population_status_counts(population)
        if (time / config["time_conversion_factor"]) % 3 == 0:
            update_graphs(population_percentage, time_list, len(population), counts[0],
                          counts[1], counts[2], time / config["time_conversion_factor"], r_vals)

def communities_movement(canvas, config):
    print("-----------------------------------------------")
    all_infections = {}
    victim_dict = {}
    quarantined = {}
    close_contacts = {}
    susceptible = {}
    infected = {}
    recovered = {}
    final_R= []
    time = 0
    population_percentage = {
        'infected': [],
        'susceptible': [],
        'recovered': []
    }
    time_list = []
    r_vals = [[], []]
    make_stackplot(population_percentage, time_list)
    make_lineplot(r_vals[0], r_vals[1])
    print("spawing communiyirs")
    population = location.spawn_people_communities(400, config["community_coordinates"], config["incubation_period"], canvas)
    iteration = 0
    for person_id in population.keys():
        population[person_id].displacement_prob = random.random()
        # population[person_id].is_infected = True
    social_dist(100, population)
    helpers.infect_random_people(population, config)
    helpers.filter_infectious(population, susceptible, infected)
    helpers.update_vaccination_and_mask_status(population, config)
    timesteps = 0
    while run_simulation == True:
        time += 1
        timesteps += 1
        quarantine_contacts = []
        # sd_factor
        canvas.update()
        movement.simulate_movement_communities(population, infected, recovered, config)
        # if timesteps == config["time_conversion_factor"]:
        helpers.calculate_infections(population, susceptible, infected, config)
        susceptible = {}
        infected = {}
        helpers.filter_infectious(population, susceptible, infected)
        helpers.update_contacts(population, close_contacts, config)
        helpers.trace_contacts(population, infected, close_contacts, config)
        counts = helpers.get_population_status_counts(population)
        if (time / config["time_conversion_factor"]) % 3 == 0:
            update_graphs(population_percentage, time_list, len(population), counts[0],
                          counts[1], counts[2], time / config["time_conversion_factor"], r_vals)
        total_infec = 0
        # for key in all_infections.keys():
        #     total_infec += all_infections[key]
        # print("All infections lenght", total_infec)
        # index += 1

def central_hub_movement(canvas, config):
    susceptible = {}
    all_infections = {}
    victim_dict = {}
    infected = {}
    recovered = {}
    close_contacts = {}
    time = 0

    population = location.spawn_people_random(225, [-250, 250],[-250, 250], config["incubation_period"], canvas)
    for person_id in population.keys():
        population[person_id].displacement_prob = random.random()
        # population[person_id].is_infected = True
    social_dist(100, population)
    helpers.infect_random_people(population, config)
    helpers.filter_infectious(population, susceptible, infected)
    helpers.update_vaccination_and_mask_status(population, config)
    timesteps = 0
    population_percentage = {
        'infected': [],
        'susceptible': [],
        'recovered': []
    }
    time_list = []
    # make_lineplot()
    r_vals = [[], []]
    make_stackplot(population_percentage, time_list)
    make_lineplot(r_vals[0], r_vals[1])
    while run_simulation == True:

        time += 1
        timesteps += 1
        quarantine_contacts = []
        # sd_factor
        canvas.update()
        movement.simulate_movement_centralHub(population, infected, recovered, config)
        # if timesteps == config["time_conversion_factor"]:
        helpers.calculate_infections(population, susceptible, infected, config)
        susceptible = {}
        infected = {}
        helpers.filter_infectious(population, susceptible, infected)
        r_vals = helpers.calculate_R(time, population, susceptible, all_infections, victim_dict, config, r_vals)
        helpers.update_contacts(population, close_contacts, config)
        counts = helpers.get_population_status_counts(population)
        if (time / config["time_conversion_factor"]) % 3 == 0:
            update_graphs(population_percentage, time_list, len(population), counts[0],
                          counts[1], counts[2], time / config["time_conversion_factor"], r_vals)

def simulate_random_movement(canvas, config):
    draw_pen = turtle.RawTurtle(canvas)
    screens.create_random_mov_screen(draw_pen)
    random_movement(canvas, config)

def simulate_communities_movement(canvas, config):
    draw_pen = turtle.RawTurtle(canvas)
    screens.create_communities_screen(draw_pen)
    communities_movement(canvas, config)

def simulate_central_hub_movement(canvas, config):
    draw_pen = turtle.RawTurtle(canvas)
    screens.create_central_hub_screen(draw_pen)
    central_hub_movement(canvas, config)

def build_gui():
    print("In am called too")
    root.geometry('1500x1500')
    canvas = tk.Canvas(master=root, width=650, height=800)
    canvas.place(x=800, y=0)
    screen = turtle.TurtleScreen(canvas)
    screen.bgcolor('black')
    screen.tracer(0)
    return screen


def runSimulation():
    # global canvas
    run_simulation = True
    canvas = build_gui()
    config = get_config_obj()
    if config[constants.environment_options_menu] == "Open":
        simulate_random_movement(canvas, config)
    elif config[constants.environment_options_menu] == "Central-hub":
        simulate_central_hub_movement(canvas, config)
    else:
        simulate_communities_movement(canvas, config)

def control_changed(*val):
    run_simulation = False
    # runSimulation(canvas)
    print("hello world", *val)

def btnClicked():
    run_simulation = False
    runSimulation()

def generate_ui_controls():
    btn = tk.Button(master=root, bg="white", fg="black", text="Start", command=btnClicked)
    virus_options = ["SARS-COV-1", "SARS-COV-2"]
    optvar_1 = StringVar(root)
    optvar_1.set(virus_options[1])
    virus_options_menu = OptionMenu(root, optvar_1, *virus_options)
    UI_ELEMENTS_MAP[constants.virus_options_menu] = optvar_1

    enviroment_options = ["Open", "Central-hub", "Communities"]
    optvar_2 = StringVar(root)
    optvar_2.set(enviroment_options[0])
    enviroment_options_menu = OptionMenu(root, optvar_2, *enviroment_options)

    UI_ELEMENTS_MAP[constants.environment_options_menu] = optvar_2
    optvar_2.trace("w", control_changed)
    scale_social_distancing = tk.Scale(orient='horizontal', from_=0, to=1)
    scale_social_distancing.bind("<ButtonRelease-1>", control_changed)
    UI_ELEMENTS_MAP[constants.social_distancing] = scale_social_distancing
    scale_population = tk.Scale(orient='horizontal', from_=100, to=800)
    scale_population.bind("<ButtonRelease-1>", control_changed)
    UI_ELEMENTS_MAP[constants.population] = scale_population
    scale_init_inf_per = tk.Scale(orient='horizontal', from_=1, to=100)
    scale_init_inf_per.bind("<ButtonRelease-1>", control_changed)
    UI_ELEMENTS_MAP[constants.initial_infection_percentage] = scale_init_inf_per
    scale_vacc_prob = tk.Scale(orient='horizontal', from_=0, to=1, resolution=0.)
    scale_vacc_prob.bind("<ButtonRelease-1>", control_changed)
    UI_ELEMENTS_MAP[constants.vaccine_probability] = scale_vacc_prob
    scale_vacc_eff = tk.Scale(orient='horizontal', from_=0, to=1, resolution=0.1)
    scale_vacc_eff.bind("<ButtonRelease-1>", control_changed)
    UI_ELEMENTS_MAP[constants.vaccine_efficacy] = scale_vacc_eff
    scale_mask_prob = tk.Scale(orient='horizontal', from_=0, to=1, resolution=0.1)
    scale_mask_prob.bind("<ButtonRelease-1>", control_changed())
    UI_ELEMENTS_MAP[constants.mask_probability] = scale_mask_prob

    # scale.place(x=40, y=70)
    # btn.place(x=10, y=20)
    # btn.grid(row=1, column=0)
    Label(root, text="Virus Options: ").grid(row=3, column=0, sticky= "E" ,padx=0)
    virus_options_menu.grid(row=3, column=1, sticky="W",padx = 0)
    Label(root, text="Environment Options: ").grid(row=3, column=2, sticky= "E" ,padx=0)
    enviroment_options_menu.grid(row=3, column=3, sticky="W",padx = 0)
    Label(root, text="Social Distancing Factor: ").grid(row=5, column=0)
    scale_social_distancing.grid(row=5, column=1)
    Label(root, text="Population: ").grid(row=6, column=0)
    scale_population.grid(row=6, column=1)
    Label(root, text="Initial Infection Percentage: ").grid(row=7, column=0)
    scale_init_inf_per.grid(row=7, column=1)
    Label(root, text="Vaccine Probability: ").grid(row=8, column=0)
    scale_vacc_prob.grid(row=8, column=1)
    Label(root, text="Vaccine Efficiency: ").grid(row=9, column=0)
    scale_vacc_eff.grid(row=9, column=1)
    Label(root, text="Mask Probability: ").grid(row=10, column=0)
    scale_mask_prob.grid(row=9, column=1)
    btn.grid(row=12, column=0)

# gs = grd.GridSpec(2, 2, height_ratios=[1,10], width_ratios=[6,1], wspace=0.1)







def isfloat(x):
    try:
        a = float(x)
    except (TypeError, ValueError):
        return False
    else:
        return True



def get_config_obj():
    conf = {}
    for key in UI_ELEMENTS_MAP.keys():
        value = UI_ELEMENTS_MAP[key].get()
        conf[key] = value
    environment_config  = parser._sections[conf[constants.virus_options_menu]]
    for key in environment_config:
        env_value = environment_config[key]
        if isfloat(env_value):
            conf[key] = float(env_value)
        elif env_value.isnumeric():
            conf[key] = int(env_value)
        else:
            conf[key] = env_value
    for key in constants.config_params.keys():
        conf[key] = constants.config_params[key]
    return conf


# communities_movement(screen)
generate_ui_controls()
runSimulation()
print("test")
# random_movement(screen)
# central_hub_movement(screen)
root.mainloop()