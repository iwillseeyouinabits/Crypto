import socket
import FileUpdater
import json
import FW
import traceback
import ast


class Server:
    def __init__(self):
        self.ip = self.get_ip_address()
        self.port = 42069
        self.ipDict = json.loads(FW.FW("IP.json").read())
        self.portOther = 42069
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def receive(self):
        fileUpdater = FileUpdater.FileUpdater()
        print(str((self.ip, self.port)) + " !!!")
        self.socket.bind((self.ip, self.port))
        print("binded")
        self.socket.listen(500)
        print("listening on port")
        while True:
            clientsocket, address = self.socket.accept()
            print("accepted connection")
            msgIn = ""
            while True:
                msgIn += clientsocket.recv(1).decode("utf-8")
                try:
                    msgIn = ast.literal_eval(msgIn)
                    print("RECEIVED!!!")
                    try:
                        fileUpdater.handleNewInfo(self.ipDict[self.get_ip_address()][0], self.ipDict[self.get_ip_address()][1], msgIn)
                        break
                    except Exception:
                        print(traceback.format_exc())
                except:
                    continue

    def connect(self, msg):
        msgOut = msg
        print("Connecting to ")
        for ip in self.ipDict:
            if not ip == self.get_ip_address():
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
    
    def correctSingleQuoteJSON(self, s):
        rstr = ""
        escaped = False

        for c in s:
        
            if c == "'" and not escaped:
                c = '"' # replace single with double quote
            
            elif c == "'" and escaped:
                rstr = rstr[:-1] # remove escape character before single quotes
            
            elif c == '"':
                c = '\\' + c # escape existing double quotes
    
            escaped = (c == "\\") # check for an escape character
            rstr += c # append the correct json
        
        return rstr