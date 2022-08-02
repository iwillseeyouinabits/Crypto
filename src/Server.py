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
        time.sleep(5)
        self.socket.bind((self.ip, self.port))
        self.socket.listen(5)
        clientsocket, address = self.socket.accept()
        print("_______________________________________________")
        msgOut = input()
        clientsocket.send(bytes(msgOut,"utf-8"))
        clientsocket.shutdown()
        clientsocket.close()
        self.socket.shutdown()
        self.socket.close()
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connect()

    def connect(self):
        time.sleep(8)
        self.socket.connect((self.ip2, self.port2))
        msgIn = self.socket.recv(2**12).decode("utf-8")
        print(" => " + msgIn)
        self.socket.shutdown()
        self.socket.close()
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.receive()