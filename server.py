# -*- coding: utf-8 -*-
import json
import socket
import threading
import model

CONNECTED_PATTERN = "Client connected: {}:{}"
END_CHARACTER = "\0"
TARGET_ENCODING = "utf-8"
M="-2"


class Server(object):

    def __init__(self):
        self.clients = set()
        self.listen_thread = None
        self.port = 8080
        self.sock = None
        self.N=0

    def listen(self):
        self.sock.listen(2)
        while True:
            try:
                client, address = self.sock.accept()
                self.N = self.N + 1
                if(self.N==1):
                    mess = model.Message(id=None,win=None,quit=True,Number="-2").marshal()
                    client.sendall(mess)
                if (self.N == 2):
                    mess = model.Message(id=None,win=None,quit=True,Number="-1").marshal()
                    client.sendall(mess)
                print(self.N)
            except OSError:
                print("Connection aborted")
                return
            print(CONNECTED_PATTERN.format(*address))
            self.clients.add(client)
            threading.Thread(target=self.handle, args=(client,)).start()

    def handle(self, client):

        while True:
            try:
                message = model.Message(**json.loads(self.receive(client)))
            except (ConnectionAbortedError, ConnectionResetError):
                print("Connection aborted")
                return
            if (message.Number=='-'):
                for client2 in self.clients:
                    if(client==client2):
                        mess = model.Message(id=None,win=None,quit=True, Number="-1").marshal()
                        client2.sendall(mess)
                    else:
                        mess = model.Message(id=None, win=None, quit=True, Number="-2").marshal()
                        client2.sendall(mess)
            else:
                if message.quit:
                    client.close()
                    self.clients.remove(client)
                    print("The client disconnected")
                    t=0
                    for client2 in self.clients:
                        mess = model.Message(id=None,win=None,quit=True, Number="-2").marshal()
                        client2.sendall(mess)
                        t=1
                    if(t==1):
                        self.N=1
                    else:
                        self.N=0
                    return
                self.broadcast(message,client)

    def broadcast(self, message,client1):
        for client in self.clients:
            if (client1 != client):
                client.sendall(message.marshal())

    def receive(self, client):
        buffer = ""
        while not buffer.endswith(END_CHARACTER):
            buffer += client.recv(2 ** 10).decode(TARGET_ENCODING)
        return buffer[:-1]

    def run(self):
        print(R"Server is running...")
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind(("", self.port))
        self.listen_thread = threading.Thread(target=self.listen)
        self.listen_thread.start()



if __name__ == "__main__":
    try:
        Server().run()
    except RuntimeError as error:
        print("Error")
        print(str(error))