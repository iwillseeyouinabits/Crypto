import socket
import json
import FileUpdater
import json
import FW


class Server:
    def __init__(self):
        self.ip = socket.gethostbyname(socket.gethostname())
        self.port = 42069
        self.ipDict = json.loads(FW.FW("IP.json").read())
        self.portOther = 42069
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
        msgOut = msg
        print("Connecting to ")
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        for ip in self.ipDict:
            print((ip, self.portOther))
            self.socket.connect((ip, self.portOther))
            self.socket.send(bytes(msgOut, "utf-8"))
            self.socket.close()