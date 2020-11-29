# -*- coding: utf-8 -*-
import json
import socket
import threading
import model
import schema
import time
import os.path

from jsonschema import validate, Draft4Validator

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
        self.obn()
        self.sock.listen(2)
        while True:
            try:
                client, address = self.sock.accept()
                self.N = self.N + 1
                if(self.N==1):
                    mess = model.Message(quit=True,Number="-2").marshal()
                    client.sendall(mess)
                if (self.N == 2):
                    mess = model.Message(quit=True,Number="-1").marshal()
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
                mess=json.loads(self.receive(client))
                message = model.Message(**mess)
            except (ConnectionAbortedError, ConnectionResetError):
                print("Connection aborted")
                return
            if(message.Save!=None):
                self.SaveIn(message,client)
            else:
                if(message.Load!=None):
                    self.LoadS(message,client)
                else:
                    if (message.Number=='-'):
                        self.obn()
                        for client2 in self.clients:
                            if(client==client2):
                                mess = model.Message(quit=True, Number="-1").marshal()
                                client2.sendall(mess)
                            else:
                                mess = model.Message(quit=True, Number="-2").marshal()
                                client2.sendall(mess)
                    else:
                        if message.quit:
                            self.obn()
                            client.close()
                            self.clients.remove(client)
                            print("The client disconnected")
                            t=0
                            for client2 in self.clients:
                                mess = model.Message(quit=True, Number="-2").marshal()
                                client2.sendall(mess)
                                t=1
                            if(t==1):
                                self.N=1
                            else:
                                self.N=0
                            return
                        self.Save(mess)
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

    def obn(self):
        f = open('JSONF.json', 'w')
        f.close()

    def SaveIn(self,message,client):
        if(os.path.exists(message.Save+".json")):
            mess = model.Message(id='0', win='0', quit=True, Number=0, idCl='1', Load="No2").marshal()#Сделать просто метод который будет такое отправлять и менять там только значение Load
            client.sendall(mess)
            return False
        try:
            with open("JSONF.json") as file:
                file_content = file.read().strip()
                if file_content:  # если нет
                    username = json.loads(file_content)
                else:
                    tt=1
                    #обработка ошибки
        except FileNotFoundError:
            return None
        except json.JSONDecodeError:  # Некорректное содержимое файла
            return None
        with open(message.Save+".json", "w") as write_file:
            json.dump(username, write_file, indent=4)


    def LoadS(self,message,client):
        username=[]
        if(len(self.clients)<2):
            mess = model.Message(id='0', win='0', quit=True, Number=0, idCl='1',
                                 Save=None, Load="No1").marshal()
            client.sendall(mess)
        if(os.path.exists(message.Load+".json")):
            try:
                with open(message.Load+".json") as file:
                    file_content = file.read().strip()
                    username = json.loads(file_content)#Сохранённые ходы

            except FileNotFoundError:
                return None
            except json.JSONDecodeError:  # Некорректное содержимое файла
                return None
            self.obn()
            if(message.idCl=='1'):
                self.vspm(client,username,message,"-1","-2","1","0")
            else:
                self.vspm(client, username, message, "-2", "-1", "0", "1")
        else:
            mess = model.Message(id='0', win='0', quit=True, Number=0, idCl='1', Load="No").marshal()
            client.sendall(mess)


    def vspm(self,client,username,message,str1,str2,str3,str4):
        for client2 in self.clients:
            if (client == client2):
                mess = model.Message(quit=True, Number=str1).marshal()
                client2.sendall(mess)
                cl1 = client2
            else:
                mess = model.Message(quit=True, Number=str2).marshal()
                client2.sendall(mess)
                cl2 = client2
        for i in range(len(username)):
            time.sleep(0.015)
            k = username[i]
            if (k['idCl'] == message.idCl):
                mess = model.Message(id='0', win='0', quit=True, Number=k['Number'], idCl=str3).marshal()
                cl1.sendall(mess)
                time.sleep(0.02)
                cl2.sendall(mess)
            else:
                mess = model.Message(id='0', win='0', quit=True, Number=k['Number'], idCl=str4).marshal()
                cl1.sendall(mess)
                time.sleep(0.02)
                cl2.sendall(mess)


    def Save(self,message):
        #Здесь должна идти проверка на схему
        if(Draft4Validator(schema.schema).is_valid(message)):
            lists=[]
            lists.append(message)
            try:
                with open("JSONF.json") as file:
                        # Читаем содержимое файла, обрезаем пробелы в начале и в конце
                        # (тогда файл содержащий только пробелы или переносы строк
                        #  будет эквивалентен пустому файлу)
                        file_content = file.read().strip()

                        # Проверяем, пустой ли файл
                        if file_content:#если нет
                            # Декодируем json
                            username = json.loads(file_content)
                            for i in range(len(lists)):
                                username.append(lists[i])
                        else:
                            username=lists

            except FileNotFoundError:
                return None
            except json.JSONDecodeError:  # Некорректное содержимое файла
                return None
            with open("JSONF.json", "w") as write_file:
                json.dump(username, write_file,indent=4)


if __name__ == "__main__":
    try:
        Server().run()
    except RuntimeError as error:
        print("Error")
        print(str(error))