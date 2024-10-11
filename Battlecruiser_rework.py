import tkinter
import random
import time #!!!

from Ship import *
#time.clock()
canvas = tkinter.Canvas(width=1200, height=1200, bg='black')
canvas.pack()

MAX_d = 1500
d = 0
time.clock = time.time
times = time.clock()

ship = Ship(500, 500, 1.0, 10000.0)
ship.core = ShipCore(100, 120000)
ship.shield = ShipShields(100)

missiles = []  # where the missiles are stored
objects = []  # where the asteroids are stored
speed_factor = 1.0

rocking = 0
delay = random.randint(100, 500)
delay = int(delay / speed_factor)

canvas.create_rectangle(1000, 0, 1200, 1000, fill='grey')  # Info panel on the right

#hull = [10000.0, None, True]  # hull hp, where the text of the hull is stored, hull ok
canvas.create_text(1100, 50, text='Hull status', font = 'Arial 20')
ship.hull_text = canvas.create_text(1100, 100, text=str(round(ship.hull_hp, 1)), font='Arial 20', fill='red')

ship.speed_text = canvas.create_text(1100, 350, text=round(ship.speed, 2), font='Arial 20', fill='red')
canvas.create_text(1100, 300, text='Speed', font = 'Arial 20') #

#core = [100-30*speed_factor, 120000, 0, 0]  # dE/dt, E, text of dE/dt, text of E
dE_dt = 100-30*ship.speed
ship.core.output_text = canvas.create_text(1100, 400, text=('Core output: '+str(round(dE_dt, 0))))
ship.core.energy_text = canvas.create_text(1100, 450, text=('Batteries: '+str(round(ship.core.energy, 0))))

ship.shield.delta_text = canvas.create_text(1100, 500, text=('shields input: '+str(round(ship.shield.delta, 1))))
#shields = [0.0, 100.0, 100.0, True, None, None, None]  # dS/dt, S, max S, S active, text dS/dt, text S, text S active
ship.shield.shield_text = canvas.create_text(1100, 550, text=('shields status: ' + str(round(ship.shield.level, 0))))
ship.shield.max_text = canvas.create_text(1100, 600, text=('shields full: '+str(round(ship.shield.max, 0))))

#canvas.create_rectangle(1000, 0, 1200, 1000, fill='grey')
ship_ok_image = tkinter.PhotoImage(file='Cruiser_engine_no_flames.png')
ship_flames_image = tkinter.PhotoImage(file='Cruiser_engine_flames.png')
asteroid10 = tkinter.PhotoImage(file='Asteroid10.png')
asteroid15 = tkinter.PhotoImage(file='Asteroid15.png')
asteroid20 = tkinter.PhotoImage(file='Asteroid20.png')
ship_image_on_canvas = canvas.create_image(ship.x, ship.y, image = ship_ok_image)


def shield(ship):
    # shields are active, not at full, and core if fine
    if ship.core.energy > 0:
        ship.shield.level = min(ship.shield.level + ship.shield.delta, ship.shield.max)


def shields_up(v):
    if ship.shield.delta <= ship.shield.max_delta - 0.1:
        ship.shield.delta = ship.shield.delta + 0.1
        canvas.delete(ship.shield.delta_text)
        ship.shield.delta_text = canvas.create_text(1100, 500,
                                                    text=('shields input: '+str(round(ship.shield.delta, 1))))


def shields_down(v):
    global core, shields
    if ship.shield.delta >= 0.1:
        ship.shield.delta = ship.shield.delta - 0.1
        canvas.delete(ship.shield.delta_text)
        ship.shield.delta_text = canvas.create_text(1100, 500,
                                                    text=('shields input: ' + str(round(ship.shield.delta, 1))))


def speed_up(v):
    if ship.speed <= 2.6 and ship.hull_hp > 0:
        ship.speed += 0.2
        canvas.delete(ship.speed_text)
        ship.speed_text = canvas.create_text(1100, 350, text=round(ship.speed, 2), font='Arial 20', fill='red')
        canvas.delete(ship.core.output_text)
        ship.core.output_text = canvas.create_text(1100, 400, text=('Core output: '+str(round(ship.core.output_text, 0))))


def slow_down(v):
    global speed_factor, speed
    if ship.speed >= 0.8 and ship.hull_hp > 0:
        ship.speed -= 0.2
        canvas.delete(ship.speed_text)
        ship.speed_text = canvas.create_text(1100, 350, text=round(ship.speed, 2), font='Arial 20', fill='red')
        canvas.delete(ship.core.output_text)
        ship.core.output_text = canvas.create_text(1100, 400,
                                                   text=('Core output: ' + str(round(ship.core.output_text, 0))))


def left(v):
    global times
    if ship.core.energy > 500 and round(time.clock(), 1) > times:
        times = round(time.clock(), 1) + 0.1
        if ship.x > 60:
            ship.x -= 3
            canvas.move(ship_image_on_canvas, -3, 0)
            ship.core.energy -= 500
            canvas.update()


def right(v):
    global times
    if ship.core.energy > 500 and round(time.clock(), 1) > times:
        times = round(time.clock(), 1) + 0.1
        if ship.x < 940:
            ship.x += 3
            canvas.move(ship_image_on_canvas, +3, 0)
            ship.core.energy -= 500
            canvas.update()


def front(v):  # front guns
    global missiles
    if ship.core.energy > 2000 and ship.hull_hp > 0:
        missiles.append([canvas.create_line(ship.x+20, ship.y-80, ship.x+20, ship.y-90, fill='red', width=3)])
        missiles[-1].append(ship.x+20)  # x
        missiles[-1].append(ship.y-80)  # y
        missiles.append([canvas.create_line(ship.x-20, ship.y-80, ship.x-20, ship.y-90, fill='red', width=3)])
        missiles[-1].append(ship.x-20)  # x
        missiles[-1].append(ship.y-80)  # y
        ship.core.energy -= 2000
        canvas.update()


def fire(variable):  # side guns
    global missiles
    if ship.core.energy > 1000 and ship.hull_hp > 0:
        missiles.append([canvas.create_line(ship.x+64, ship.y-20, ship.x+64, ship.y-30, fill='red', width=2)])
        missiles[-1].append(ship.x+64)  # x
        missiles[-1].append(ship.y-20)  # y
        missiles.append([canvas.create_line(ship.x-60, ship.y-20, ship.x-60, ship.y-30, fill='red', width=2)])
        missiles[-1].append(ship.x-60)  # x
        missiles[-1].append(ship.y-20)  # y
        ship.core.energy -= 1000
        canvas.update()


def collision():
    global missiles, objects, canvas
    i = 0
    while i < len(missiles):
        # for each missile check every object for collision
        j = 0
        missile_hit = False
        while j < len(objects):
            if (objects[j][1]-objects[j][4] <= missiles[i][1] <= objects[j][1]+objects[j][4] and
                    objects[j][2]-objects[j][4] <= missiles[i][2]-10 <= objects[j][2]+objects[j][4]):
                missile_hit = True
                canvas.delete(missiles[i][0])
                missiles.remove(missiles[i])
                objects[j][3] -= 1
                if objects[j][3] == 0:
                    canvas.delete(objects[j][0])
                    objects.remove(objects[j])
                break
            j += 1
        if missile_hit:
            continue
        i += 1
    # check every surviving object if it collides with the ship
    i = 0
    while i < len(objects):
        if (objects[i][1]+objects[i][4] >= ship.x-60 and objects[i][1]-objects[i][4] <= ship.x+64 and
                objects[i][2]+objects[i][4] >= ship.y-100 and objects[i][2]+objects[i][4] <= ship.y+50 and
                ship.shield.level <= 0):
            ship.hull_hp -= objects[i][3] * ship.speed * 1000
            objects[i][3] = 0
            canvas.delete(ship.hull_text)
            ship.hull_text = canvas.create_text(1100, 100, text=round(ship.hull_hp, 1), font='Arial 20', fill='red')
        elif (objects[i][1]+objects[i][4] >= ship.x-60 and objects[i][1]-objects[i][4] <= ship.x+64 and
              objects[i][2]+objects[i][4] >= ship.y-100 and objects[i][2]+objects[i][4] <= ship.y+50 and
              ship.shield.level > 0):
            ship.shield.level -= objects[i][3] * 20
            objects[i][3] = 0
            if ship.shield.level > ship.shield.max:
                ship.shield.level = ship.shield.max
            if ship.shield.level < 0:
                # carry over the dmg to the hull
                ship.hull_hp += ship.shield.level * ship.speed * 50
                ship.shield.level = 0
                canvas.delete(ship.hull_text)
                ship.hull_text = canvas.create_text(1100, 100, text=round(ship.hull_hp, 1), font='Arial 20', fill='red')
            canvas.delete(ship.shield.shield_text)
            ship.shield.shield_text = canvas.create_text(1100, 550,
                                                         text=('shields status: '+str(round(ship.shield.level, 0))))
        if objects[i][3] == 0:
            canvas.delete(objects[i][0])
            objects.remove(objects[i])
        else:
            i += 1
    if ship.hull_hp <= 0:
        canvas.delete('all')
        canvas.create_text(600, 400, text=round(d, 1), font='Arial 30', fill='blue')


def move():
    global missiles, objects, d, rocking, delay, ship_image_on_canvas

    if rocking == 100:
        canvas.delete(ship_image_on_canvas)
        ship_image_on_canvas = canvas.create_image(ship.x, ship.y, image = ship_ok_image)
    elif rocking == 0:
        canvas.delete(ship_image_on_canvas)
        ship_image_on_canvas = canvas.create_image(ship.x, ship.y, image = ship_flames_image)

    if ship.hull_hp > 0:
        d += speed_factor
        if d >= MAX_d:
            canvas.delete('all')
            canvas.create_text(600, 400, text='Finish', font='Arial 30', fill='blue')
    for i in range(len(missiles)):
        #canvas.update()
        canvas.move(missiles[i][0], 0, -10)
        missiles[i][2] -= 10
    i = 0
    while i < len(missiles):
        if missiles[i][2] <= 0:
            canvas.delete(missiles[i][0])
            missiles.remove(missiles[i])
        else:
            i += 1
    #canvas.update()
    i = 0
    while i < len(objects):
        #canvas.update()
        canvas.move(objects[i][0], 0, +5*ship.speed)
        objects[i][2]+=(5*ship.speed)
        if objects[i][2] >= 1000:
            #print('Objects', objects)
            canvas.delete(objects[i][0])
            objects.remove(objects[i])
        else:
            i += 1
    ship.core.output = ship.core.base_output - (ship.speed*30 + ship.shield.delta*100)
    canvas.delete(ship.core.output_text)
    ship.core.output_text = canvas.create_text(1100, 400, text=('Core output: '+str(round(ship.core.output, 0))))
    #canvas.delete(core[3])
    #core[3] = canvas.create_text(1100, 550, text=('Batteries:',round(core[1], 0)))
    ship.core.energy = min(ship.core.energy + ship.core.output, ship.core.max_energy)
    if 0 < ship.core.energy <= ship.core.max_energy:
        ship.core.energy = min(ship.core.energy + ship.core.output, ship.core.max_energy)
    elif ship.core.energy <= 0 and ship.core.output < 0:
        ship.hull_hp += ship.core.output*10
    canvas.delete(ship.core.energy_text) #
    ship.core.energy_text = canvas.create_text(1100, 450,
                                               text=('Batteries: '+str(round(ship.core.energy, 0))))
    if ship.shield.level < ship.shield.max and ship.core.energy > 0:
        ship.shield.level = min(ship.shield.level + ship.shield.delta, ship.shield.max)
        canvas.delete(ship.shield.shield_text)
        ship.shield.shield_text = canvas.create_text(1100, 550,
                                                     text=('shields status: '+str(round(ship.shield.level, 0))))

    shield(ship)
    collision()          
    canvas.update()
    if rocking >= delay:
        x = random.randint(20, 980)
        r = random.choice((10, 15, 20))
        if r == 10:
            objects.append([canvas.create_image(x,0, image = asteroid10)])
            objects[-1].append(x)
            objects[-1].append(0)
            objects[-1].append(random.randint(1, 4))  # object's durability
            objects[-1].append(r)
        elif r == 15:
            objects.append([canvas.create_image(x,0, image = asteroid15)])
            objects[-1].append(x)
            objects[-1].append(0)
            objects[-1].append(random.randint(3, 6))
            objects[-1].append(r)
        elif r == 20:
            objects.append([canvas.create_image(x,0, image = asteroid20)])
            objects[-1].append(x)
            objects[-1].append(0)
            objects[-1].append(random.randint(5, 8))
            objects[-1].append(r)
        rocking = 0
        delay = random.randint(100, 500)
        delay = int(delay / speed_factor)
    else:
        rocking += 10
        
    if ship.hull_hp > 0 and d < MAX_d:
        canvas.after(10, move)

canvas.bind_all('<space>', fire)
canvas.bind_all('<a>', left) # maybe use lambda functions
canvas.bind_all('<d>', right) #
canvas.bind_all('<w>', speed_up)
canvas.bind_all('<s>', slow_down)
canvas.bind_all('<q>', shields_down)
canvas.bind_all('<e>', shields_up)
canvas.bind_all('<f>', front)

canvas.update()
move()
input()
