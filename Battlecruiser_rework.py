import tkinter
import random
import time #!!!
#time.clock()
canvas = tkinter.Canvas(width=1200, height=1200, bg='black')
canvas.pack()

d = 0
time.clock = time.time
times = time.clock()

position = [500, 500]  # ship's position
missiles = []  # where the missiles are stored
objects = []  # where the asteroids are stored
speed_factor = 1.0

rocking = 0
delay = random.randint(100, 500)
delay = int(delay / speed_factor)

canvas.create_rectangle(1000, 0, 1200, 1000, fill='grey')  # Info panel on the right

hull = [10000.0, None, True]  # hull hp, where the text of the hull is stored, hull ok
canvas.create_text(1100, 50, text='Hull status', font = 'Arial 20')
hull[1] = canvas.create_text(1100, 100, text=str(round(hull[0], 1)), font='Arial 20', fill='red')

speed = [speed_factor]
speed.append(canvas.create_text(1100, 350, text=speed[0], font='Arial 20', fill='red')) #
canvas.create_text(1100, 300, text='Speed', font = 'Arial 20') #

core = [100-30*speed_factor, 120000, 0, 0]  # dE/dt, E, text of dE/dt, text of E
core[2] = canvas.create_text(1100, 400, text=('Core output: '+str(round(core[0], 0)))) #Toto píše v {}.
core[3] = canvas.create_text(1100, 450, text=('Batteries: '+str(round(core[1], 0)))) #Toto píše normálne

shields = [0.0, 100.0, 100.0, True, None, None, None]  # dS/dt, S, max S, S active, text dS/dt, text S, text S active
shields[4] = canvas.create_text(1100, 500, text=('shields input: '+str(round(shields[0], 1)))) #Toto tiež.
shields[5] = canvas.create_text(1100, 550, text=('shields status: '+str(round(shields[1], 0)))) #Toto tiež.
shields[6] = canvas.create_text(1100, 600, text=('shields full: '+str(round(shields[2], 0)))) #Toto tiež.

#canvas.create_rectangle(1000, 0, 1200, 1000, fill='grey')
ship_ok_image = tkinter.PhotoImage(file='Cruiser_engine_no_flames.png')
ship_flames_image = tkinter.PhotoImage(file='Cruiser_engine_flames.png')
asteroid10 = tkinter.PhotoImage(file='Asteroid10.png')
asteroid15 = tkinter.PhotoImage(file='Asteroid15.png')
asteroid20 = tkinter.PhotoImage(file='Asteroid20.png')
ship_image_on_canvas = canvas.create_image(position[0], position[1], image = ship_ok_image)


def shield():
    # shields are active, not at full, and core if fine
    if shields[3] and shields[1] < shields[2] and core[1] > 0:
        shields[1] += shields[0]
        shields[1] = min(shields[1] + shields[0], shields[2])


def shields_up(v):
    global core, shields
    if shields[0] <= 0.4:
        shields[0] += 0.1
        canvas.delete(shields[4])
        shields[4] = canvas.create_text(1100, 500, text=('shields input: '+str(round(shields[0], 1))))


def shields_down(v):
    global core, shields
    if shields[0] >= 0.1:
        shields[0] -= 0.1
        canvas.delete(shields[4])
        shields[4] = canvas.create_text(1100, 500, text=('shields input: '+str(round(shields[0], 1))))


def speed_up(v):
    global speed_factor, speed
    if speed_factor < 2.6 and hull[2] == True:
        speed_factor += 0.2
        speed[0] = speed_factor
        canvas.delete(speed[1])
        speed[1] = canvas.create_text(1100, 350, text=round(speed[0], 2), font='Arial 20', fill='red')
        #core[0]=100-30*speed_factor
        canvas.delete(core[2])
        core[2] = canvas.create_text(1100, 400, text=('Core output: '+str(round(core[0], 0))))


def slow_down(v):
    global speed_factor, speed
    if speed_factor >= 0.8 and hull[2] == True:
        speed_factor -= 0.2
        speed[0] = speed_factor
        canvas.delete(speed[1])
        speed[1] = canvas.create_text(1100, 350, text=round(speed[0], 2), font='Arial 20', fill='red')
        #core[0]=100-30*speed_factor
        canvas.delete(core[2])
        core[2] = canvas.create_text(1100, 400, text=('Core output: '+str(round(core[0], 0))))


def left(v):
    global position, ship_image_on_canvas, times
    if core[1] > 500 and round(time.clock(), 1) > times: #energia potrebna na posun
        times = round(time.clock(), 1) + 0.1
        if position[0] > 60:
            position[0] -= 3
            canvas.move(ship_image_on_canvas, -3, 0)
            core[1] -= 500
            canvas.update()


def right(v):
    global position, ship_image_on_canvas, times
    if core[1] > 500 and round(time.clock(), 1) > times: #energia potrebna na posun
        times = round(time.clock(), 1) + 0.1
        if position[0] < 940:
            position[0] += 3
            canvas.move(ship_image_on_canvas, +3, 0)
            core[1] -= 500
            canvas.update()


def front(v):  # front guns
    global missiles, core
    if core[1] > 2000 and hull[2] == True: #energia potrebna na strely
        missiles.append([canvas.create_line(position[0]+20, position[1]-80, position[0]+20, position[1]-90, fill='red', width=3)]) #Pridanie pravej strely
        missiles[-1].append(position[0]+20) #prevdepodobne x-ova suradnica
        missiles[-1].append(position[1]-80) #prevdepodobne y-ova suradnica
        missiles.append([canvas.create_line(position[0]-20, position[1]-80, position[0]-20, position[1]-90, fill='red', width=3)]) #Pridanie lavej strely
        missiles[-1].append(position[0]-20) #prevdepodobne x-ova suradnica
        missiles[-1].append(position[1]-80) #prevdepodobne y-ova suradnica
        core[1] -= 2000
        canvas.update()


def fire(variable):  # side guns
    global missiles, core
    if core[1] > 1000 and hull[2] == True:
        missiles.append([canvas.create_line(position[0]+64, position[1]-20, position[0]+64, position[1]-30, fill='red', width=2)]) #Pridanie pravej strely
        missiles[-1].append(position[0]+64)  # x
        missiles[-1].append(position[1]-20)  # y
        missiles.append([canvas.create_line(position[0]-60, position[1]-20, position[0]-60, position[1]-30, fill='red', width=2)]) #Pridanie lavej strely
        missiles[-1].append(position[0]-60)  # x
        missiles[-1].append(position[1]-20)  # y
        core[1] -= 1000
        canvas.update()


def collision():
    global missiles, objects, position, hull, speed_factor, shields, canvas
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
        if objects[i][1]+objects[i][4] >= position[0]-60 and objects[i][1]-objects[i][4] <= position[0]+64 and objects[i][2]+objects[i][4] >= position[1]-100 and objects[i][2]+objects[i][4] <= position[1]+50 and not shields[3]:
            hull[0] -= objects[i][3] * speed_factor * 1000
            objects[i][3] = 0
            canvas.delete(hull[1])
            hull[1] = canvas.create_text(1100, 100, text=round(hull[0], 1), font='Arial 20', fill='red')
        elif objects[i][1]+objects[i][4] >= position[0]-60 and objects[i][1]-objects[i][4] <= position[0]+64 and objects[i][2]+objects[i][4] >= position[1]-100 and objects[i][2]+objects[i][4] <= position[1]+50 and shields[3]:
            shields[1] -= objects[i][3] * 20
            objects[i][3] = 0
            if shields[1] > shields[2]:
                shields[1] = shields[2]
            if shields[1] < 0:
                hull[0] += shields[1] * speed_factor * 50
                shields[1] = 0
                canvas.delete(hull[1])
                hull[1] = canvas.create_text(1100, 100, text=round(hull[0], 1), font='Arial 20', fill='red')
            canvas.delete(shields[5])
            shields[5] = canvas.create_text(1100, 550, text=('shields status: '+str(round(shields[1], 0))))
        if objects[i][3] == 0:
            canvas.delete(objects[i][0])
            objects.remove(objects[i])
        else:
            i += 1
    if hull[0] <= 0:
        hull[2] = False
        canvas.delete('all')
        canvas.create_text(600, 400, text=round(d, 1), font='Arial 30', fill='blue')


def move():
    global missiles, objects, core, shields, d, hull, speed_factor, rocking, delay, ship_image_on_canvas

    if rocking == 100:
        canvas.delete(ship_image_on_canvas)
        ship_image_on_canvas = canvas.create_image(position[0], position[1], image = ship_ok_image)
    elif rocking == 0:
        canvas.delete(ship_image_on_canvas)
        ship_image_on_canvas = canvas.create_image(position[0], position[1], image = ship_flames_image)

    if hull[0] > 0:
        d += speed_factor
        if d >= 1500:
            hull[2] = False
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
        canvas.move(objects[i][0], 0, +5*speed_factor)
        objects[i][2]+=(5*speed_factor)
        if objects[i][2] >= 1000:
            #print('Objects', objects)
            canvas.delete(objects[i][0])
            objects.remove(objects[i])
        else:
            i += 1
    core[0] = 100-(speed_factor*30 + shields[0]*100)
    canvas.delete(core[2])
    core[2] = canvas.create_text(1100, 400, text=('Core output: '+str(round(core[0], 0))))
    #canvas.delete(core[3])
    #core[3] = canvas.create_text(1100, 550, text=('Batteries:',round(core[1], 0)))
    if 0 < core[1] <= 120000:
        core[1] = min(core[1] + core[0], 120000)
    elif core[1] <= 0 and core[0] < 0:
        hull[0] += core[0]*10
    canvas.delete(core[3]) #
    core[3] = canvas.create_text(1100, 450, text=('Batteries: '+str(round(core[1], 0))))
    if shields[1] < shields[2] and core[1] > 0:
        shields[1] += shields[0]
        canvas.delete(shields[5])
        shields[5] = canvas.create_text(1100, 550, text=('shields status: '+str(round(shields[1], 0))))

    shield()
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
        
    if hull[2] == True:
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
