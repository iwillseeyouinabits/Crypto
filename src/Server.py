import socket
import time

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
            msgOut = input("=> ")
            if msgOut == "CLOSE":
                self.socket.close()
                clientsocket.close()
                break
            clientsocket.send(bytes(msgOut,"utf-8"))
            msgIn = clientsocket.recv(2**12).decode("utf-8")
            print(" => " + msgIn)
            

    def connect(self):
        self.socket.connect((self.ip2, self.port2))
        while True:
            msgIn = self.socket.recv(2**12).decode("utf-8")
            print(" => " + msgIn)
            msgOut = input("=> ")
            if msgOut == "CLOSE":
                self.socket.close()
                break
            self.socket.send(bytes(msgOut, "utf-8"))