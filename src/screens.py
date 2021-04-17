import turtle

def draw_square(start_coordinates, side_length, draw_pen):
    draw_pen.penup()
    draw_pen.setposition(start_coordinates[0], start_coordinates[1])
    draw_pen.pendown()
    for i in range(4):
        draw_pen.fd(side_length)
        draw_pen.lt(90)
    draw_pen.hideturtle()

def set_default_config(draw_pen, color="white", pen_size = 1):
    draw_pen.speed(0)
    draw_pen.color(color)
    draw_pen.pensize(pen_size)

def create_quarantine_location(start_coordinates, side_length, draw_pen):
    set_default_config(draw_pen, "red", 5)
    draw_square(start_coordinates, side_length, draw_pen)

def create_random_mov_screen(draw_pen):
    set_default_config(draw_pen)
    draw_square([-250, -250], 500, draw_pen)


def create_central_hub_screen(draw_pen):
    set_default_config(draw_pen)
    draw_square([-250, -250], 500, draw_pen)
    draw_square([-20, -20], 20, draw_pen)

def create_communities_screen(draw_pen):
    set_default_config(draw_pen)
    draw_square([-300, -300], 620, draw_pen)
    draw_square([-280, 120], 180, draw_pen)
    draw_square([-80, 120], 180, draw_pen)
    draw_square([120, 120], 180, draw_pen)
    draw_square([-280, -80], 180, draw_pen)
    draw_square([-80, -80], 180, draw_pen)
    draw_square([120, -80], 180, draw_pen)
    draw_square([-280, -280], 180, draw_pen)
    draw_square([-80, -280], 180, draw_pen)
    draw_square([120, -280], 180, draw_pen)