import turtle
from turtle import *

if __name__ == "__main__":

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


    def square(x, y, name):
        """
        Graphic function - presenting a picture/text on the screen
        :param x: x coordinate on the screen
        :param y: y coordinate on the screen
        :param name: picture's name
        :return: none
        """
        wn = Screen()
        if name.endswith('.gif'):
            wn.register_shape(name)
            tr = Turtle(shape=name)
            tr.up()
            tr.goto(x, y)
            tr.stamp()


    def do_border():
        setheading(270)
        delay(0)
        for tile in tiles:
            penup()
            goto(tile[0] - 105, tile[1] + 105)
            pendown()
            for i in range(4):
                forward(210)
                left(90)


    setup(1920, 1080, 0, 0)
    hideturtle()

    t = turtle.Turtle()
    t.penup()
    t.goto(-400, 300)
    t.pendown()
    t.write(arg="circle", font=("Ariel", 28, "bold"), align="center")
    do_border()
    # square(-400, 300, 'rectangle.gif')
    mainloop()