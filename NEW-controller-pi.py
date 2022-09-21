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
from time import sleep
import turtle
from turtle import *


YOUR_TURN = "your turn"
NOT_YOUR_TURN = "not your turn"

shapes = [
    'circle',
    'triangle',
    'star',
    'hexagon',
    'square',
    'rhombus',
    'rectangle',
    'pentagon',
]

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

ips = ['192.168.0.45',  '192.168.0.64', '192.168.0.42', '192.168.0.155']  # static ips
connections = []
points = 0
curr = 0
curr_idx = 0
last_idx = 0
level = 0


def create_sequence(count: int):
    """
    Creates the sequence of the shapes randomly
    count - num of shapes (num of level)
    """
    used = []
    seq = ""
    for i in range(0, count):
        rand = random.randrange(0, 8)
        while rand in used:
            rand = random.randrange(0, 8)
        seq += shapes[rand] + ";"
        used.append(rand)
    return seq[:-1]


def show_seq(seq: str):
    seq_list = seq.split(';')
    for i in range(len(seq_list)):
        draw_img(tiles[i][0], tiles[i][1], seq_list[i])
    update()


def draw_img(x, y, name):
    wn = Screen()
    name += '.gif'
    wn.register_shape(name)
    tr = Turtle(shape=name)
    tr.up()
    tr.goto(x, y)
    tr.stamp()


def change_num(level: int, failed: bool = False):
    global curr, points
    if failed:
        curr = 0
    elif curr == level:
        curr = 0
        return True
    draw_img(50, -300, numbers[curr + 1])
    update()
    curr += 1
    return False


def fail():
    Screen().bgcolor("red")
    sleep(2)
    Screen().bgcolor("white")


def success():
    Screen().bgcolor("green")
    sleep(2)
    Screen().bgcolor("white")


def get_port(ip: str):
    os.system("rm ./port.txt")
    os.system(f"sshpass -p 'Ninja@2022' scp simonpi@{ip}:/home/simonpi/Desktop/simon-py/port.txt ./port.txt")
    f = open("./port.txt", 'r')
    port = int(f.readline())
    print(port)
    return port


def configure_button(x: int, y: int, txt: str):
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


def next_clicked(x, y):
    global curr_idx, last_idx, level, points
    connections[curr_idx].sendall('K'.encode())
    if change_num(level):
        success()
        points += level
        while curr_idx == last_idx:
            curr_idx = random.randrange(0, 3)
        last_idx = curr_idx
        reload_level()


def fail_clicked(x, y):
    global curr_idx, level
    connections[curr_idx].sendall('F'.encode())
    fail()
    change_num(level, True)


def restart_clicked(x, y):
    global curr_idx, level, curr, points
    connections[curr_idx].sendall('R'.encode())

    # show points
    Screen().clearscreen()
    turtle.write("You gained " + str(points) + " Points!", font=("Verdana", 50, "normal"), align="center")
    hideturtle()
    sleep(10)
    print("Points - " + str(points))
    Screen().clearscreen()

    # set up the buttons on the screen
    tracer(True)
    delay(0)
    setup_buttons()

    curr = 0
    level = 0
    points = 0
    reload_level()


def is_msg_sent(sent):
    if sent:
        return True
    return False


def setup_buttons():
    # configure buttons
    next_button = configure_button(-400, -300, "next")
    next_button.onclick(next_clicked)
    fail_button = configure_button(-500, -300, "fail")
    fail_button.onclick(fail_clicked)
    restart_button = configure_button(-600, -300, "restart")
    restart_button.onclick(restart_clicked)


def reload_level():
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
    seq = create_sequence(level)

    # send the sequence to the showing screen

    # UPDATE - NEW PROTOCOL
    # LEVEL_NUMBER & OPTION(IMG, TXT-NAMES, TXT-COLORS, QR-NAMES, QR-COLORS) & SEQUENCE

    # EXAMPLE: 2&TXT-COLORS&red;green
    # EXAMPLE: 4&QR-NAMES&rectangle;triangle;circle;square
    # EXAMPLE: 3&IMG&star;rhombus;pentagon

    sock.sendall((str(level) + seq).encode())

    # show the sequence on the screen
    show_seq(seq)
    change_num(level)


def start():
    global curr, points, level, curr_idx, last_idx

    # set up screen
    setup(1920, 1080, 0, 0)

    # configure connections
    for ip in ips:
        port = get_port(ip)
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((ip, port))
        connections.append(sock)

    # choose random screen
    curr_idx = random.randrange(0, 3)
    last_idx = curr_idx

    # reload first level

    # set up the buttons on the screen
    tracer(True)
    delay(0)
    setup_buttons()
    reload_level()


if __name__ == "__main__":
    start()
    mainloop()

