import socket
import json
import struct
import fcntl
import FileUpdater
import json

from src import FW


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
    def get_ip_address(self, ifname):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        return socket.inet_ntoa(fcntl.ioctl(
            s.fileno(),
            0x8915,  # SIOCGIFADDR
            struct.pack('256s', ifname[:15])
        )[20:24])