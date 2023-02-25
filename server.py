import socket
import threading 

#Constants
HEADER = 64
PORT = 5050
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"
PING = "ping"
NOTHING = "nothing"

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)
msg_list = []
msg_dict = {}


def handle_client(conn, addr,msg_list, msg_dict):
    print(f"[NEW CONNECTION] {addr} connected.")

    connected = True
    while connected:
        msg_length = conn.recv(HEADER).decode(FORMAT)
        if msg_length:
            msg_length = int(msg_length)
            msg = conn.recv(msg_length).decode(FORMAT)
            key = msg[0]
            msg = msg[1:]
            if msg == PING:
                if msg_dict == {}:
                    conn.send(PING.encode(FORMAT))
                else:
                    for i in msg_dict:
                        if i != key:
                            new_msg = (msg_dict[i]).encode(FORMAT)
                            conn.send(new_msg)
                    msg_dict.pop(i)
            else:
                msg_dict[key] = msg
                msg_list.append(msg)
                conn.send(NOTHING.encode(FORMAT))

            if msg == DISCONNECT_MESSAGE:
                msg_dict = {}
                connected = False

    print(f"[DISCONNECTED] {addr} disconnected")
    conn.close()

def start():
    server.listen()
    print(f"[LISTENING] Server is listening on {SERVER}")
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr, msg_list,msg_dict))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 1}")

print("[STARTING] server is starting...")
start()