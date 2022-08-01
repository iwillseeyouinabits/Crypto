import socket

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
        print("Send Message to " + str((self.ip2, self.port2)) + "  =>")
        msgOut = input()
        clientsocket.send(bytes(msgOut,"utf-8"))
        print("SENT")
        clientsocket.close()
        self.socket.close()
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connect()

    def connect(self):
        self.socket.connect((self.ip2, self.port2))
        msgIn = self.socket.recv(2**12).decode("utf-8")
        print("Message from "  + str((self.ip2, self.port2)) + " reads => " + msgIn)
        self.socket.close()
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.receive()