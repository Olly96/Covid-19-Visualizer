
import turtle
import random

class Person:

    def __init__(self, person_id, x_limit, y_limit, incubation_period, particle_size,  canvas):
        self.id = person_id
        self.is_ever_infected = False
        self.infected_by = "None"
        self.is_quarantined = False
        self.displacement_prob = 1
        self.is_moving = False
        self.x_limit = x_limit
        self.y_limit = y_limit
        self.is_moving_dest = False
        self.is_moving_home = False
        self.x_dest = 0
        self.y_dest = 0
        self.is_central_hub = False
        self.status = "S"
        self.infected_time = 0
        self.close_contacts = []
        self.particle_size = particle_size
        self.incubation_period = incubation_period
        self.infection_probability = 0
        self.vaccination_status = False
        self.vaccine_efficacy = "None"
        self.mask_status = False
        self.update_prob_tracker = 0
        self.turtle = turtle.RawTurtle(canvas)
        self.initialize_turtle()

    def initialize_turtle(self):
        self.turtle.shape('circle')
        self.turtle.shapesize(self.particle_size)
        self.turtle.color('#4183C4')
        self.turtle.penup()
        self.turtle.speed(0)
        x = random.randint(self.x_limit[0], self.x_limit[1])
        y = random.randint(self.y_limit[0], self.y_limit[1])
        self.turtle.setposition(x, y)
