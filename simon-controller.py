import socket
import os

# Controlling center of Simon game
os.system("rm ./port.txt")
os.system("sshpass -p 'Aa123456' scp pi@192.168.0.42:/home/pi/Desktop/simon-py/port.txt ./port.txt")

RP_IP = '192.168.0.42'

f = open("./port.txt", 'r')
port = int(f.readline())
print(port)
# CHANGE THE PORT TO THE PORT APPEARING ON THE SCREEN

# There are 4 different types of messages to send:
#   'K' - Success (continuing to the next shape)
#   'F' - Failure (restarting level)
#   'R' - Restart (restarting game)
#   'Q' - Quit (quiting game)

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((RP_IP, port))
while True:
    msg = input("Enter command: ")
    sock.sendall(msg.encode())
    if msg == 'Q':
        break
