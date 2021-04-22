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
root.title('Covid 19 Visualizer')
parser = ConfigParser()
GUI_CONFIG_PARAMS = {}
UI_ELEMENTS_MAP = {}
run_simulation = True
screens = screens.screen()
movement = movement.Movement()
parser.read('dev.ini')


def make_stackplot(stack_percentage_obj, tl):
    fig, ax = plt.subplots(figsize=(3.9, 3.9))
    ax.stackplot(tl, stack_percentage_obj.values(),
                 labels=stack_percentage_obj.keys())
    ax.legend(loc='upper left')
    ax.set_title('SIR Stack plot')
    ax.set_xlabel('Time')
    ax.set_ylabel('Percentage')
    fig.tight_layout()
    canvas_stackplot = FigureCanvasTkAgg(fig,
                                         master=root)
    canvas_stackplot.get_tk_widget().grid(row=0, column=0, padx=(0, 0), pady=(0, 0))

def make_lineplot(time, r_values):
    fig, ax = plt.subplots(figsize=(3.9, 3.9))
    ax.plot(time, r_values)
    ax.set_title('R-Factor')
    ax.set_xlabel('Time(Days)')
    ax.set_ylabel('Rt')
    fig.tight_layout()
    canvas_lineplot = FigureCanvasTkAgg(fig,
                                         master=root)
    canvas_lineplot.draw()

    canvas_lineplot.get_tk_widget().grid(row=0, column=1, padx=(0, 0), pady=(0, 0))


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
    close_contacts = {}
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
    population = location.spawn_people_random(config, [-250, 250], [-250, 250], canvas)
    for person_id in population.keys():
        population[person_id].displacement_prob = random.random()
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
        if config[constants.contact_tracing_status] == "True":
            helpers.update_contacts(population, close_contacts, config)
            helpers.trace_contacts(population, infected, close_contacts, config)
        counts = helpers.get_population_status_counts(population)
        if (time / config["time_conversion_factor"]) % 3 == 0:
            update_graphs(population_percentage, time_list, len(population), counts[0],
                          counts[1], counts[2], time / config["time_conversion_factor"], r_vals)


def communities_movement(canvas, config):
    close_contacts = {}
    susceptible = {}
    infected = {}
    recovered = {}
    all_infections = {}
    victim_dict = {}
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
    population = location.spawn_people_communities(config, canvas)
    for person_id in population.keys():
        population[person_id].displacement_prob = random.random()
    helpers.infect_random_people(population, config)
    helpers.filter_infectious(population, susceptible, infected)
    helpers.update_vaccination_and_mask_status(population, config)
    timesteps = 0
    while run_simulation == True:
        time += 1
        timesteps += 1
        canvas.update()
        movement.simulate_movement_communities(population, infected, recovered, config)
        helpers.calculate_infections(population, susceptible, infected, config)
        susceptible = {}
        infected = {}
        helpers.filter_infectious(population, susceptible, infected)
        r_vals = helpers.calculate_R(time, population, susceptible, all_infections, victim_dict, config, r_vals)
        if config[constants.contact_tracing_status] == "True":
            helpers.update_contacts(population, close_contacts, config)
            helpers.trace_contacts(population, infected, close_contacts, config)
        counts = helpers.get_population_status_counts(population)
        if (time / config["time_conversion_factor"]) % 3 == 0:
            update_graphs(population_percentage, time_list, len(population), counts[0],
                          counts[1], counts[2], time / config["time_conversion_factor"], r_vals)


def central_hub_movement(canvas, config):
    susceptible = {}
    all_infections = {}
    victim_dict = {}
    infected = {}
    recovered = {}
    close_contacts = {}
    time = 0
    population = location.spawn_people_random(config, [-250, 250],[-250, 250], canvas)
    for person_id in population.keys():
        population[person_id].displacement_prob = random.random()
    helpers.infect_random_people(population, config)
    helpers.filter_infectious(population, susceptible, infected)
    helpers.update_vaccination_and_mask_status(population, config)
    population_percentage = {
        'infected': [],
        'susceptible': [],
        'recovered': []
    }
    time_list = []
    r_vals = [[], []]
    make_stackplot(population_percentage, time_list)
    make_lineplot(r_vals[0], r_vals[1])
    while run_simulation == True:

        time += 1

        canvas.update()
        movement.simulate_movement_centralHub(population, infected, recovered, config)
        helpers.calculate_infections(population, susceptible, infected, config)
        susceptible = {}
        infected = {}
        helpers.filter_infectious(population, susceptible, infected)
        r_vals = helpers.calculate_R(time, population, susceptible, all_infections, victim_dict, config, r_vals)

        if config[constants.contact_tracing_status] == "True":
            helpers.update_contacts(population, close_contacts, config)
            helpers.trace_contacts(population, infected, close_contacts, config)
        counts = helpers.get_population_status_counts(population)
        if (time / config["time_conversion_factor"]) % 1 == 0:
            update_graphs(population_percentage, time_list, len(population), counts[0],
                          counts[1], counts[2], time / config["time_conversion_factor"], r_vals)

def simulate_random_movement(canvas, config):
    draw_pen = turtle.RawTurtle(canvas)
    screens.create_random_mov_screen(draw_pen)
    if config[constants.contact_tracing_status] == "True":
        screens.create_quarantine_location(draw_pen)
    random_movement(canvas, config)

def simulate_communities_movement(canvas, config):
    draw_pen = turtle.RawTurtle(canvas)
    screens.create_communities_screen(draw_pen)
    if config[constants.contact_tracing_status] == "True":
        screens.create_quarantine_location(draw_pen)
    communities_movement(canvas, config)

def simulate_central_hub_movement(canvas, config):
    draw_pen = turtle.RawTurtle(canvas)
    screens.create_central_hub_screen(draw_pen)
    if config[constants.contact_tracing_status] == "True":
        screens.create_quarantine_location(draw_pen)
    central_hub_movement(canvas, config)

def build_gui():
    root.geometry('1500x1500')
    canvas = tk.Canvas(master=root, width=650, height=800)
    canvas.place(x=800, y=0)
    screen = turtle.TurtleScreen(canvas)
    screen.bgcolor('black')
    screen.tracer(0)
    return screen


def runSimulation():
    # global canvas
    global run_simulation
    run_simulation = True
    canvas = build_gui()
    config = get_config_obj()
    if config[constants.environment_options_menu] == "Open":
        simulate_random_movement(canvas, config)
    elif config[constants.environment_options_menu] == "Central-hub":
        simulate_central_hub_movement(canvas, config)
    else:
        simulate_communities_movement(canvas, config)

def start_button_clicked():
    global run_simulation
    run_simulation = False
    runSimulation()

def stop_button_clicked():
    global run_simulation
    run_simulation = False

def generate_ui_controls():
    startBtn = tk.Button(master=root, bg="white", fg="black", text="Start", command=start_button_clicked)
    stopBtn = tk.Button(master=root, bg="white", fg="black", text="Stop", command=stop_button_clicked)

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

    contact_tracing_options = ["True", "False"]
    optvar_3 = StringVar(root)
    optvar_3.set(contact_tracing_options[1])
    contact_tracing_options_menu = OptionMenu(root, optvar_3, *contact_tracing_options)
    UI_ELEMENTS_MAP[constants.contact_tracing_status] = optvar_3

    scale_social_distancing = tk.Scale(orient='horizontal', from_=0, to=1, resolution=0.1)
    UI_ELEMENTS_MAP[constants.social_distancing] = scale_social_distancing
    scale_population = tk.Scale(orient='horizontal', from_=100, to=800)
    scale_population.set(200)
    UI_ELEMENTS_MAP[constants.population] = scale_population
    scale_init_inf_per = tk.Scale(orient='horizontal', from_=1, to=100)
    scale_init_inf_per.set(6)
    UI_ELEMENTS_MAP[constants.initial_infection_percentage] = scale_init_inf_per
    scale_vacc_prob = tk.Scale(orient='horizontal', from_=0, to=1, resolution=0.)
    scale_vacc_prob.set(0)
    UI_ELEMENTS_MAP[constants.vaccine_probability] = scale_vacc_prob
    scale_vacc_eff = tk.Scale(orient='horizontal', from_=0.65, to=1, resolution=0.01)
    UI_ELEMENTS_MAP[constants.vaccine_efficacy] = scale_vacc_eff
    scale_mask_prob = tk.Scale(orient='horizontal', from_=0, to=1, resolution=0.1)
    UI_ELEMENTS_MAP[constants.mask_probability] = scale_mask_prob
    scale_particle_size = tk.Scale(orient='horizontal', from_=0.05, to=0.3, resolution=0.05)
    scale_particle_size.set(0.15)
    UI_ELEMENTS_MAP[constants.particle_size] = scale_particle_size

    # scale.place(x=40, y=70)
    # btn.place(x=10, y=20)
    # btn.grid(row=1, column=0)
    Label(root, text="Virus Options: ").grid(row=3, column=0, sticky= "E" ,padx=0)
    virus_options_menu.grid(row=3, column=1, sticky="W",padx = 0)
    Label(root, text="Environment Options: ").grid(row=4, column=0, sticky= "E" ,padx=0)
    enviroment_options_menu.grid(row=4, column=1, sticky="W",padx = 0)
    Label(root, text="Social Distancing Factor: ").grid(row=5, column=0, sticky= "E" ,padx=0)
    scale_social_distancing.grid(row=5, column=1, sticky="W",padx = 0)
    Label(root, text="Population: ").grid(row=6, column=0, sticky= "E" ,padx=0)
    scale_population.grid(row=6, column=1, sticky="W",padx = 0)
    Label(root, text="Initial Infection Percentage: ").grid(row=7, column=0, sticky= "E" ,padx=0)
    scale_init_inf_per.grid(row=7, column=1, sticky="W",padx = 0)
    Label(root, text="Vaccine Probability: ").grid(row=8, column=0, sticky= "E" ,padx=0)
    scale_vacc_prob.grid(row=8, column=1, sticky="W",padx = 0)
    Label(root, text="Vaccine Efficiency: ").grid(row=9, column=0, sticky= "E" ,padx=0)
    scale_vacc_eff.grid(row=9, column=1, sticky="W",padx = 0)
    Label(root, text="Mask Probability: ").grid(row=10, column=0, sticky= "E" ,padx=0)
    scale_mask_prob.grid(row=10, column=1, sticky="W",padx = 0)
    Label(root, text="Particle Size: ").grid(row=11, column=0, sticky= "E" ,padx=0)
    scale_particle_size.grid(row=11, column=1, sticky = "W", padx=0)
    Label(root, text="Contact Tracing: ").grid(row=12, column=0, sticky= "E" ,padx=0)
    contact_tracing_options_menu.grid(row=12, column=1, sticky = "W", padx=0)
    startBtn.grid(row=13, column=0, sticky= "E" ,padx=0, pady=10)
    stopBtn.grid(row=13, column=1, sticky= "W" ,padx=0, pady=10)


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
    environment_config = parser._sections[conf[constants.virus_options_menu]]
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
# random_movement(screen)
# central_hub_movement(screen)
root.mainloop()
