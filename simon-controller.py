import socket

# Controlling center of Simon game

RP_IP = '192.168.0.42'

# CHANGE THE PORT TO THE PORT APPEARING ON THE SCREEN
PORT = 52237

# There are 4 different types of messages to send:
#   'K' - Success (continuing to the next shape)
#   'F' - Failure (restarting level)
#   'R' - Restart (restarting game)
#   'Q' - Quit (quiting game)

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((RP_IP, PORT))
while True:
    msg = input("Enter command: ")
    sock.sendall(msg.encode())
    if msg == 'Q':
        break

