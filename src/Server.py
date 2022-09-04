import socket
import json
import FileUpdater
import IP.json
class Server:

    def __init__(self):
        self.ip =
        self.port = 42069
        self.ip2 = ip2
        self.port2 = 42404
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def receive(self):
        fileUpdater = FileUpdater.FileUpdater()
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
                    fileUpdater.handleNewInfo(msgIn)
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