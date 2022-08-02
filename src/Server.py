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
        msgOut = input("=> ")
        clientsocket.send(bytes(msgOut,"utf-8"))
        clientsocket.shutdown(socket.SHUT_RDWR)
        self.socket.shutdown(socket.SHUT_RDWR)
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connect()

    def connect(self):
        self.socket.connect((self.ip2, self.port2))
        msgIn = self.socket.recv(2**12).decode("utf-8")
        print(" => " + msgIn)
        self.socket.shutdown(socket.SHUT_RDWR)
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.receive()