import random
import socket
import os
from time import sleep

YOUR_TURN = "your turn"
NOT_YOUR_TURN = "not your turn"

# Controlling center of Simon game

# CHANGE THE PORT TO THE PORT APPEARING ON THE SCREEN

# There are 4 different types of messages to send:
#   'K' - Success (continuing to the next shape)
#   'F' - Failure (restarting level)
#   'R' - Restart (restarting game)
#   'Q' - Quit (quiting game)


ips = ['192.168.0.45',  '192.168.0.64', '192.168.0.155', '192.168.0.42']  # static ips
connections = []


def get_port(ip: str):
    os.system("rm ./port.txt")
    os.system(f"sshpass -p 'Ninja@2022' scp simonpi@{ip}:/home/simonpi/Desktop/simon-py/port.txt ./port.txt")
    f = open("./port.txt", 'r')
    port = int(f.readline())
    print(port)
    return port


def start():
    for ip in ips:
        port = get_port(ip)
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((ip, port))
        connections.append(sock)
    curr_idx = random.randrange(0, 4)
    last_idx = curr_idx
    res = ""
    while True:
        for conn_sock in connections:
            if conn_sock == connections[curr_idx]:
                conn_sock.sendall("your turn".encode())
            else:
                conn_sock.sendall("not your turn".encode())
        while res != "finished":
            msg = input("Enter command: ")
            for conn_sock in connections:
                conn_sock.sendall(msg.encode())
                res = conn_sock.recv(1024).decode()
        while curr_idx == last_idx:
            curr_idx = random.randrange(0, 4)
        last_idx = curr_idx
        res = ""
        if msg == 'Q':
            break


if __name__ == "__main__":
    start()
