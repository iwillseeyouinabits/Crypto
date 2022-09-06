import socket
import FileUpdater
import json
import FW


class Server:
    def __init__(self):
        self.ip = self.get_ip_address()
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
                    fileUpdater.handleNewInfo(self.ipDict[self.get_ip_address()][0], self.ipDict[self.get_ip_address()][1], msgIn)
                    break
                except:
                    continue

    def connect(self, msg):
        msgOut = msg
        print("Connecting to ")
        for ip in self.ipDict:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.connect((ip, self.portOther))
            self.socket.send(bytes(msgOut, "utf-8"))
            self.socket.close()
            print("sent too => " + str((ip, self.portOther)))


    def get_ip_address(self):
        import socket
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        return s.getsockname()[0]