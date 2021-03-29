import turtle
import random
import math

# def main():
#     wn = turtle.Screen()
#     alex = turtle.Turtle()
#     alex.forward(150)
#     alex.left(90)
#     alex.forward(75)
#     wn.exitonclick()
# if __name__=='__main__':
#     main()
odd_number_as_sqrt_of_population = 15
# If we use an odd number, the balls will not go to the edge with social distancing and every position will be used as you see

infection_prob = 100
# infection_prob = the probability of one infecting another when they collide
population = odd_number_as_sqrt_of_population ** 2
# The total population is the square root of the variable odd_number_as_sqrt_of_population
recovery_time = 100
# the recovery time stand for how long it takes every infected ball/person to recover and no longer be contagious (when they're no longer contagious, they turn gray)
social_distancing = False
start_sd = 30
# start_sd = the amount of people that have to be infected before social distancing kicks in, some people get infected while moving to the social distancing spot
sd_p = 100
# sd_p is the percentage of people that participate in social distancing
quarantaine_on = True
time_until_q = 3000
# we can even turn on social distancing and quarantaine on the same time...

wn = turtle.Screen()
wn.bgcolor('black')
wn.title('Epidemic simulator')
wn.tracer(0)
print("I am here")
# the part above creates the screen that pops up when we run the code. To make everything work, allways use wn.mainloop() at the end.

pen = turtle.Turtle()
pen.speed(0)
pen.color('white')
pen.penup()
pen.setposition(-200, -200)
pen.pendown()
pen.pensize(3)
for i in range(4):
    pen.fd(400)
    pen.lt(90)
pen.hideturtle()
# this part creates the white square

time = 0
balls = []
# balls is the list containing all the balls
infected = []
# the list infected contains all balls that got infected (red and gray).
time_infected = {}
tot_inf = []
# same as infected, without duplicates
recovered = []
# recovered contains all balls that are recovered (gray).
closest_ball = []
spaces_x = []
spaces_y = []
coordinates = []
# coordinates contains all coordinates available for the social distancing

for i in range(-200, 201):
    if i % int(400 / math.sqrt(
            population)) == 0:  # this is a calculation I created to make sure that more coordinates are created with a larger population
        # the weird population value, using the square of an odd number is part of this calculation.
        spaces_x.append(i)
        spaces_y.append(i)

for x in spaces_x:
    for y in spaces_y:
        coordinate = [x, y]
        coordinates.append(coordinate)

for _ in range(population):
    balls.append(turtle.Turtle())
    # this part appends a turtle to the list balls

for ball in balls:
    ball.shape('circle')
    ball.shapesize(0.45, 0.45)
    ball.color('#4183C4')
    ball.penup()
    ball.speed(0)
    x = random.randint(-190, 190)
    y = random.randint(-190, 190)
    ball.goto(x, y)
    ball.dx = random.choice(
        [-3, -2.75, -2.5, -2.25, -2, -1.75, -1.5, -1.25, -1, -0.75, -0.5, -0.25, 3, 2.75, 2.5, 2.25, 2, 1.75, 1.5, 1.25,
         1, 0.75, 0.5, 0.25])
    ball.dy = random.choice(
        [-3, -2.75, -2.5, -2.25, -2, -1.75, -1.5, -1.25, -1, -0.75, -0.5, -0.25, 3, 2.75, 2.5, 2.25, 2, 1.75, 1.5, 1.25,
         1, 0.75, 0.5, 0.25])
    # here we add some information to that turtle, shape, coordinates, color, size and its dx and dy, the dx and dy are the changes in x and y for every ball
    # together they are the speed and direction of every ball. They are chosen randomly from the list using random.

    # Now we want 1 ball to become red (infected), preferably the one closest to the coordinate (0,0)

infections = {i: 0 for i in balls}


# infections is a dictionary containing every ball from balls and setting its value to 0


def closest_to_O():
    global closest_ball

    min_dist = 0
    for x in range(len(balls)):

        xdist = balls[x].xcor()
        ydist = balls[x].ycor()
        dist_squared = xdist * xdist + ydist * ydist
        if len(closest_ball) == 0:
            closest_ball.append(balls[x])
            min_dist = dist_squared
        elif dist_squared < min_dist:
            closest_ball.clear()
            closest_ball.append(balls[x])
            min_dist = dist_squared
    # this function checks which ball is closest to the coordinate (0,0) and appends it to the list closest_ball
    # so the list closest_ball has length 1 and contains only the ball closest to (0,0)


def mark_infected():
    global closest_ball

    if closest_ball[0] not in recovered:
        closest_ball[0].color('red')
        infected.append(closest_ball[0])
    # this function marks the ball closest to (0,0) as infected by adding it to the list infected and making its color red.


def collide():
    global infection_prob

    for i in range(len(balls)):

        for x in range(i + 1, len(balls)):

            xdist = balls[i].xcor() - balls[x].xcor()
            ydist = balls[i].ycor() - balls[x].ycor()
            dist_squared = xdist * xdist + ydist * ydist
            if dist_squared < 125:
                if balls[i] not in recovered and balls[x] not in recovered:
                    # I added this if statement because recovered balls can not infect other balls
                    if balls[i] in infected and balls[x] not in infected and random.randint(0, 100) in range(0,
                                                                                                             infection_prob + 1):
                        balls[x].color('red')
                        infected.append(balls[x])
                    elif balls[i] not in infected and balls[x] in infected and random.randint(0, 100) in range(0,
                                                                                                               infection_prob + 1):
                        balls[i].color('red')
                        infected.append(balls[i])
                        # the balls turn red and are added to the list infected
    # the collide function check if balls collide and infects uninfected balls when they collide with an infected one.


def recovered_():
    global population, recovery_time

    for i in range(len(balls)):
        if balls[i] in infected:
            infections[balls[i]] += 1
            # everytime that the computer runs trough this for loop, the value of the ball in infections increases by 1
            if balls[i] not in recovered:
                if infections[balls[i]] >= recovery_time:
                    balls[i].color('gray')
                    recovered.append(balls[i])
    # here we see that recovered balls turn gray and are added to the list recovered.


def social_dist():
    min_dist = 0
    closest_dist = []

    for i in range(len(balls)):

        if balls[i].xcor() > -250:
            # this line above is only for quarantaine mode

            if random.randint(0, 100) in range(0, sd_p + 1):

                for c in coordinates:

                    xdist = balls[i].xcor() - c[0]
                    ydist = balls[i].ycor() - c[1]
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
                    balls[i].dx = 0
                    balls[i].dy = 0
                    balls[i].goto(closest_dist[0], closest_dist[1])

                closest_dist.clear()


def quarantaine():
    global time_infected

    room = turtle.Turtle()
    room.speed(0)
    room.color('white')
    room.penup()
    room.setposition(-360, -210)
    room.pendown()
    room.pensize(3)
    for i in range(4):
        room.fd(120)
        room.lt(90)
    room.hideturtle()
    # this draws a room for infected people

    for i in infected:

        if i.xcor() >= -350 and i.xcor() <= -250 and i.ycor() >= -200 and i.ycor() <= -100:
            i.dx = 0
            i.dy = 0
            i.setposition(random.randint(-350, -250), random.randint(-200, -100))
            time_infected[i] = 0

        elif i not in time_infected.keys():
            time_infected[i] = time
            # this makes the value of an infected ball in the dictionary time_infected, the time when the ball gets infected
        elif i in time_infected.keys():
            if time - time_infected[i] >= time_until_q and i.xcor() > -250:
                # if the time that they are infected is larger or equal to the time until quarantaine (time_until_q)
                dx_q = (random.randint(-275, -225) - i.xcor()) * (-1)
                dy_q = random.randint(-175, -125) - i.ycor()
                try:
                    rc = dy_q / dx_q
                    if -4 < rc < 4:
                        i.dx = -10
                        i.dy = 10 * rc
                    else:
                        i.dx = 0
                        i.dy = 0
                        i.goto(random.randint(-350, -250), random.randint(-200, -100))
                        time_infected[i] = 0
                    # the direction and speed of the ball is set to go to the created quarantaine room
                except:
                    i.dx = 0
                    i.dy = 0
                    i.goto(random.randint(-350, -250), random.randint(-200, -100))
                    time_infected[i] = 0
                time_infected[i] = 0


closest_to_O()
mark_infected()

# this part makes every ball move and has almost all functions in it to make sure they're constantly checked.
while True:

    wn.update()
    # this updates the screen every time

    for ball in balls:

        time += 1

        ball.sety(ball.ycor() + ball.dy)
        ball.setx(ball.xcor() + ball.dx)
        # the two lines above move the balls

        if ball.xcor() < -195 or ball.xcor() > 195:
            ball.dx *= -1

        if ball.ycor() < -195 or ball.ycor() > 195:
            ball.dy *= -1
            # both of the if statements make sure that the balls change direction when they hit the edge of the white square

    collide()
    recovered_()

    if social_distancing and len(tot_inf) >= start_sd:
        # this only allows social distancing to happen if social_distancing is True and there are enough people infected to start social distancing.
        social_dist()

    if quarantaine_on:
        quarantaine()

    for i in infected:
        if i not in tot_inf:
            tot_inf.append(i)
        # the list tot_inf contains every element in infected, without duplicates.

    if len(recovered) < len(tot_inf):
        print('\n', 'Percentage infected:', len(tot_inf) / population * 100, '\n',
              'Infected people:', len(tot_inf), '\n', 'Recovered people:', len(recovered), '\n', 'Time:', time,
              'minutes')
        # this prints information about the simulation while there are still unrecovered infected balls/people.
    if len(recovered) == len(tot_inf) and len(recovered) > 0:
        message = 'Percentage infected: ' + str(len(tot_inf) / population * 100) + '\n' + 'Infected people: ' + str(
            len(tot_inf)) + '\n' + 'Recovered people: ' + str(len(recovered)) + '\n' + 'Time: ' + str(time) + ' minutes'
        end_message = turtle.Turtle()
        end_message.speed(0)
        end_message.color('white')
        end_message.penup()
        end_message.setposition(-190, 205)
        end_message.pendown()
        end_message.pensize(10)
        end_message.write(message, font=('style', 18, 'bold'))
        end_message.hideturtle()
        break
        # This shows the same statistics as above at the end of the simulation (when all the infected people are recovered). It also stops the while loop at that point

wn.mainloop()