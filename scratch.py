import turtle
from turtle import *
import qrcode

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

def square(x: 0, y: 200, name):
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


def square_qr_data(seq):
    data = '  '.join(seq.split(';'))
    print(data)
    data_t = Turtle()
    delay(0)
    data_t.penup()
    data_t.sety(-200)
    data_t.write(arg=data, font=("Ariel", 30, "bold"), align="center")
    data_t.hideturtle()

if __name__ == "__main__":

    setup(1920, 1080, 0, 0)
    hideturtle()
    create_qr("data1;data2;data3;data4;data5;data6;data7;data8", 8)
    square(0, 200, 'qr_8.gif')
    square_qr_data('data1;data2;data3;data4;data5;data6;data7;data8')
    mainloop()