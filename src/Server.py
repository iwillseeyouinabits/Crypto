import socket
import json

class Server:

    def __init__(self, ip, port, ip2, port2):
        self.ip = ip
        self.port = port
        self.ip2 = ip2
        self.port2 = port2
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def receive(self):
        self.socket.bind((self.ip, self.port))
        self.socket.listen(5)
        clientsocket, address = self.socket.accept()
        while True:
            while True:
                msgOut = input("=> ")       
                if msgOut == "CLOSE":
                    self.socket.close()
                    clientsocket.close()
                    return
                try:
                    json.loads(msgOut)
                    clientsocket.send(bytes(msgOut,"utf-8"))
                    break
                except:
                    continue
            msgIn = ""
            while True:
                msgIn += clientsocket.recv(1).decode("utf-8")
                try:
                    msgIn = json.loads(msgIn)
                    msgIn = str(msgIn)
                    break
                except:
                    continue
            print(" => " + msgIn)
            

    def connect(self):
        self.socket.connect((self.ip2, self.port2))
        while True:
            msgIn = ""
            while True:
                msgIn += self.socket.recv(1).decode("utf-8")
                try:
                    msgIn = json.loads(msgIn)
                    msgIn = str(msgIn)
                    break
                except:
                    continue
            print(" => " + msgIn)
            while True:
                msgOut = input("=> ")
                if msgOut == "CLOSE":
                    self.socket.close()
                    return
                try:
                    json.loads(msgOut)
                    self.socket.send(bytes(msgOut, "utf-8"))
                    break
                except:
                    continue