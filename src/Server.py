import socket
import json

class Server:

    def __init__(self, ip, ip2):
        self.ip = ip
        self.port = 42022
        self.ip2 = ip2
        self.port2 = 42022
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def receive(self):
            print((self.ip, self.port))
            self.socket.bind((self.ip, self.port))
            self.socket.listen(500)
            while True:
                clientsocket, address = self.socket.accept()
                msgIn = ""
                while True:
                    msgIn += clientsocket.recv(1).decode("utf-8")
                    try:
                        msgIn = json.loads(msgIn)
                        msgIn = str(msgIn)
                        print(" => " + msgIn)
                        break
                    except:
                        continue

    def connect(self, msg):
        print((self.ip2, self.port2))
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((self.ip2, self.port2))
        msgOut = msg
        json.loads(msgOut)
        self.socket.send(bytes(msgOut, "utf-8"))
        self.socket.close()