# Controlling center of Simon game

# CHANGE THE PORT TO THE PORT APPEARING ON THE SCREEN

# There are 4 different types of messages to send:
#   'K' - Success (continuing to the next shape)
#   'F' - Failure (restarting level)
#   'R' - Restart (restarting game)
#   'Q' - Quit (quiting game)

import random
import socket
import os
import time
from time import sleep
from tkinter import NONE
import turtle
from turtle import *
import keyboard
import qrcode
from threading import Thread

clicked = False
started = False
time_ground = 0

seq_options = ['IMG', 'NAMES', 'COLORS']

shapes = {
    'IMG': [
        'circle.gif',
        'triangle.gif',
        'star.gif',
        'octagon.gif',
        'square.gif',
        'rhombus.gif',
        'rectangle.gif',
        'pentagon.gif'
    ],

    'NAMES': [
        'circle',
        'triangle',
        'star',
        'octagon',
        'square',
        'rhombus',
        'rectangle',
        'pentagon'
    ],

    'COLORS': [
        'red',
        'yellow',
        'pink',
        'brown',
        'purple',
        'orange',
        'green',
        'blue'
    ]
}


numbers = {
    1: 'one.gif',
    2: 'two.gif',
    3: 'three.gif',
    4: 'four.gif',
    5: 'five.gif',
    6: 'six.gif',
    7: 'seven.gif',
    8: 'eight.gif'
}

tiles = [
    (-400, 300),
    (-100, 300),
    (200, 300),
    (500, 300),
    (-400, 0),
    (-100, 0),
    (200, 0),
    (500, -0)
]


ips = ['192.168.0.45', '192.168.0.42', '192.168.0.155', '192.168.0.64']  # static ips ,
connections = []
points = 0
curr = 0
curr_idx = 0
last_idx = 0
level = 0


def draw_border():
    """
    Creating borders on screen for the text
    :return: none
    """
    setheading(270)
    delay(0)
    for tile in tiles:
        penup()
        goto(tile[0] - 105, tile[1] + 105)
        pendown()
        for i in range(4):
            forward(210)
            left(90)


def create_sequence():
    """
    Create the sequence of the shapes randomly
    :return: sequence of shapes
    """
    ###

    # UPDATE - NEW PROTOCOL
    # LEVEL_NUMBER & OPTION(IMG, TXT-NAMES, TXT-COLORS, QR-NAMES, QR-COLORS) & SEQUENCE

    # EXAMPLE: 2&TXT-COLORS&red;green
    # EXAMPLE: 4&QR-NAMES&rectangle;triangle;circle;square
    # EXAMPLE: 3&IMG&star;rhombus;pentagon

    ###
    global level
    used = []
    seq = ""
    seq_mode = seq_options[random.randrange(0, 3)]
    for i in range(0, level):
        rand = random.randrange(0, 8)
        while rand in used:
            rand = random.randrange(0, 8)
        seq += shapes[seq_mode][rand] + ";"
        used.append(rand)

    option = ''
    if seq_mode == 'IMG':
        option = 'IMG'
    else:
        is_qr = bool(random.getrandbits(1))
        if is_qr:
            option = 'QR-' + seq_mode
        else:
            option = 'TXT-' + seq_mode
    print(str(level) + '&' + option + '&' + seq[:-1])
    return str(level) + '&' + option + '&' + seq[:-1]


def create_qr(seq: str, level: int):  # the level is a comfort thing only (for the qr name)
    """
    Create a qr code with data and saves it as a gif
    :param seq: the sequence of text to get the data from
    :param level: current level - used only for the name of the saved file
    :return: path to the qr code
    """
    data = ""
    qr = qrcode.QRCode(version=1, box_size=10, border=3)
    for name in seq.split(';'):
        data += name + '\n'
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill='black', back_color='white')
    path = f'qr_{str(level)}.gif'
    img.save(path)
    return path


def show_seq(seq: str):
    """
    Present the sequence by sending each shape to 'square' function
    :param seq: the sequence to present
    :return: none
    """
    level, mode, shapes_seq = seq.split('&')
    if 'QR' in mode:
        path = create_qr(shapes_seq, level)
        square(0, 200, path)
        square_qr_data(shapes_seq)
        update()
        return
    if 'TXT' in mode:
        color("black")
        draw_border()
    seq_list = shapes_seq.split(';')
    for i in range(len(seq_list)):
        square(tiles[i][0], tiles[i][1], seq_list[i])
    
    penup()
    goto(1900, 1080)
    color("white")
    
    update()


def square(x, y, name):
    """
    Graphic function - presenting a picture/text on the screen
    :param x: x coordinate on the screen
    :param y: y coordinate on the screen
    :param name: picture's name / text to write
    :return: none
    """
    wn = Screen()
    if name.endswith('.gif'):
        if 'qr' not in name:
            name = 'sources/' + name
        wn.register_shape(name)
        tr = Turtle(shape=name)
        tr.up()
        tr.goto(x, y)
        tr.stamp()
    else:
        penup()
        goto(x, y)
        pendown()
        write(arg=name, font=("Ariel", 28, "bold"), align="center")
        penup()


def square_qr_data(seq):
    data = '  '.join(seq.split(';'))
    print(data)
    data_t = Turtle()
    delay(0)
    data_t.penup()
    data_t.sety(-180)
    data_t.write(arg=data, font=("Ariel", 30, "bold"), align="center")
    data_t.hideturtle()

def change_num(level: int, failed: bool = False):
    """
    Updating the current number on the screen, depends on current state
    :param level: current level
    :param failed: a boolean flag ment to restart current level if failed
    :return: True if level finished, otherwise false
    """
    global curr, points
    if failed:
        curr = 0
    elif curr == level:
        curr = 0
        return True
    square(50, -300, numbers[curr + 1])
    update()
    curr += 1
    return False


def fail():
    """
    Graphic function - changing the background color to red when failing
    :return: none
    """
    Screen().bgcolor("red")
    sleep(2)
    Screen().bgcolor("white")


def success():
    """
    Graphic function - changing the background green when succeeding
    :return: none
    """
    Screen().bgcolor("green")
    sleep(2)
    Screen().bgcolor("white")
    Screen().clearscreen()
    # set up the buttons on the screen
    tracer(True)
    delay(0)
    setup_buttons()


def get_port(ip: str):
    """
    Network function - reaching for the raspberry pi to get his listening port from a local file
    :param ip: the ip of the raspberry pi
    :return: raspberry pi's listening port
    """
    os.system("rm ./port.txt")
    os.system(f"sshpass -p 'Ninja@2022' scp simonpi@{ip}:/home/simonpi/Desktop/simon-py/port.txt ./port.txt")
    f = open("./port.txt", 'r')
    port = int(f.readline())
    print(port)
    return port


def configure_game_button(x: int, y: int, txt: str):
    """
    Graphic function - configuring a buttton on the screen
    :param x: x coordinate on the screen
    :param y: y coordinate on the screen
    :param txt: text to be written on top of the button
    :return: button object
    """
    button = Turtle()
    button.hideturtle()
    button.shape('circle')
    button.shapesize(3)
    button.fillcolor('red')
    button.penup()
    button.goto(x, y)
    button.write(txt, align='center', font=('Arial', 20, 'bold'))
    button.sety(y + 70)
    button.showturtle()
    return button


def configure_start_button():
    global started
    started = False
    button = Turtle()
    # text = Turtle()

    button.shape('circle')
    button.shapesize(20)
    button.fillcolor('green')
    button.penup()
    button.goto(0, 0)
    button.showturtle()
    button.onclick(start)  
    # text.sety(-40)
    # text.write("START", align='center', font=('Arial', 60, 'bold'))
    # text.hideturtle()

def back_clicked(e):
    """
    keyboard callback - when backspace clicked returning to previous state
    :param e: event arguments(can be ignored)
    :return: none
    """
    global curr_idx, curr
    if curr - 1 == 0:
        return
    connections[curr_idx].sendall('B'.encode())
    curr -= 2
    change_num(level)


def next_clicked(x=None, y=None):
    """
    Button callback - when next clicked sending next and continuing for the next shape
    :param x: x coordinate clicked on the screen
    :param y: y coordinate clicked on the screen
    :return: none
    """
    global curr_idx, last_idx, level, points
    global clicked
    if clicked:
        return
    clicked = True

    # prevent Enter Holding bug
    while keyboard.is_pressed("Enter"):
        sleep(0.1)

    connections[curr_idx].sendall('K'.encode())
    if change_num(level):
        success()
        points += level
        while curr_idx == last_idx:
            curr_idx = random.randrange(0, 4)
        last_idx = curr_idx
        reload_level()
    clicked = False


def fail_clicked(x=None, y=None):
    """
    Button callback - when fail clicked sending fail and restarting current level
    :param x: x coordinate clicked on the screen
    :param y: y coordinate clicked on the screen
    :return: none
    """
    global clicked
    if clicked:
        return
    clicked = True
    global curr_idx, level
    connections[curr_idx].sendall('F'.encode())
    fail()
    change_num(level, True)
    clicked = False


def restart_clicked(x=None, y=None):
    """
    Button callback - when restart clicked sending restart, preseting points and restarting game
    :param x: x coordinate clicked on the screen
    :param y: y coordinate clicked on the screen
    :return: none
    """
    global clicked, time_ground
    if clicked:
        return
    clicked = True
    global curr_idx, level, curr, points, last_idx
    connections[curr_idx].sendall('R'.encode())
    total_time = time.time() - time_ground
    # show points
    Screen().clearscreen()
    
    # following line can be deleted after practice ends
    turtle.write("You gained " + str(points) + " Points!\nTimer - " + str(round(total_time, 2)), font=("Verdana", 50, "normal"), align="center")
    
    hideturtle()
    sleep(10)
    print("Points - " + str(points))
    Screen().clearscreen()

  
    curr = 0
    level = 0
    points = 0
    while curr_idx == last_idx:
        curr_idx = random.randrange(0, 4)
    last_idx = curr_idx
    configure_start_button()
    clicked = False


def setup_buttons():
    """
    Setting up the buttons on the screen and linking them with their callbacks
    :return: none
    """
    # configure buttons
    next_button = configure_game_button(-400, -300, "next")
    next_button.onclick(next_clicked)
    fail_button = configure_game_button(-500, -300, "fail")
    fail_button.onclick(fail_clicked)
    restart_button = configure_game_button(-600, -300, "restart")
    restart_button.onclick(restart_clicked)


def reload_level():
    """
    reloading new level
    """
    global curr, level, curr_idx

    tracer(False)
    curr = 0

    # define the current socket
    sock = connections[curr_idx]

    # increase level
    level += 1
    if level > 8:
        level = 8

    # create the sequence
    seq = create_sequence()

    # send the sequence to the showing screen
    print('Sending - ' + seq)
    sock.sendall(seq.encode())


    # show the sequence on the screen
    show_seq(seq)
    change_num(level)


def next_handler():
    global started
    while True:
        keyboard.wait("Enter")
        print("Enter clicked")
        if started:
            next_clicked()


def init():
    """
    Starting the program (setting up the screen, connecting to the raspberry pis, setting up buttons...)
    :return:
    """
    global curr, points, level, curr_idx, last_idx, time_ground

    # set up screen
    setup(1920, 1150, 0, 0)
    th = Thread(target=next_handler)
    th.start()
    # configure connections
    for ip in ips:
        port = get_port(ip)
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((ip, port))
        connections.append(sock)

    # choose random screen
    curr_idx = random.randrange(0, 4)
    last_idx = curr_idx
    configure_start_button()


def start(x: None, y:None):
    # reload first level
    global time_ground, started
    Screen().clearscreen()
    # set up the buttons on the screen
    tracer(True)
    delay(0)
    setup_buttons()
    started = True
    
    keyboard.on_press_key("Backspace", back_clicked)
    time_ground = time.time()
    reload_level()


if __name__ == "__main__":
    delay(0)
    init()
    mainloop()
