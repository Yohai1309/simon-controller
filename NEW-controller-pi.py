
from turtle import *

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



def start(x:None, y:None):
    write(arg="STARTED", font=("Ariel", 28, "bold"), align="center")

setup(1920, 1150, 0, 0)

button = Turtle()
text = Turtle()
text.penup()
delay(0)

button.shape('circle')
button.shapesize(20)
button.fillcolor('green')
button.penup()
button.goto(0, 0)
button.onclick(start)  
text.onclick(start)
text.write("START", align='center', font=('Arial', 60, 'bold'))

mainloop()