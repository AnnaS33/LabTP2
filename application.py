import json
import socket
import threading
import model
import CrossZero

BUFFER_SIZE = 2 ** 10


class Application(object):

    def __init__(self):
        self.closing = False
        self.host = None
        self.port = None
        self.receive_worker = None
        self.sock = None
        self.ui = CrossZero.Btn(self)
        self.N=None

    def execute(self):
        if not self.ui.startplay():
            return
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.sock.connect((self.host, self.port))  # подключаемся
        except (socket.error, OverflowError):
            print("Не получилось")
            return
        self.receive_worker = threading.Thread(target=self.receive)
        self.receive_worker.start()
        self.ui.loop()

    def receive(self):
        while True:
            try:
                message = model.Message(**json.loads(self.receive_all()))
            except (ConnectionAbortedError, ConnectionResetError):
                if not self.closing:
                    print("Error")
                return
            if(message.Number=="-1"):
                self.ui.Stop()
                self.ui.CrOrNo=1
                self.N =0
            else:
                if (message.Number == "-2"):
                    self.ui.Stop()
                    self.ui.CrOrNo = 0
                    self.N =1
                else:
                    self.ui.show_message(message)
                    self.N =0

    def receive_all(self):
        buffer = ""
        while not buffer.endswith(model.END_CHARACTER):
            buffer += self.sock.recv(BUFFER_SIZE).decode(model.TARGET_ENCODING)
        return buffer[:-1]

    def send(self, message):
        if len(message) == 0:
            return
        message = model.Message(id=message[0],win=message[1],quit=False,Number=message[2])
        try:
            self.sock.sendall(message.marshal())
        except (ConnectionAbortedError, ConnectionResetError):
            if not self.closing:
                print("Error")

    def exit(self):
        self.closing = True
        try:
            self.sock.sendall(model.Message(id=None,win=None,quit=True,Number=0).marshal())
        except (ConnectionResetError, ConnectionAbortedError, OSError):
            print("Could not connect to server")
        finally:
            self.sock.close()