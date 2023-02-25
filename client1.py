import socket
import time

HEADER = 64
PORT = 5050
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"
SERVER = "192.168.1.174"
ADDR = (SERVER, PORT)
PING = "ping"
NOTHING = "nothing"
CLIENT = 1

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)


def send(msg):
    message = (str(CLIENT) + msg).encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    client.send(send_length)
    client.send(message)
    recv = client.recv(2048).decode(FORMAT)
    if recv == PING:
        pass
    elif recv == NOTHING:
        pass    
    else:
        print("RECIEVE: ",recv)



connected = True
while connected:
    send(PING)
    msg = input("SEND: ")
    if msg == DISCONNECT_MESSAGE:
        connected = False 
    send(msg)
    time.sleep(10)
