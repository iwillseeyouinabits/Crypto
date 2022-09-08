import FileUpdater
import Server
import json
import FW
import threading

class API:
    def __init__(self, name):
        kesFile = FW.FW("keys.json")
        kes = json.loads(kesFile.read())
        kesFile.close()
        self.nSend = kes[name]["sk"][0]
        self.eSend = kes[name]["sk"][1]
        self.dSend = kes[name]["sk"][2]
        self.pSend = kes[name]["sk"][3]
        self.qSend = kes[name]["sk"][4]
        self.kes = kes

    def mine(self, numZeros=5):
        FileUpdater.FileUpdater().mine(numZeros, self.nSend, self.eSend)
    
    def addCurrency(self, name, tokens):
        FileUpdater.FileUpdater().addCurrency(self.nSend, self.eSend, self.dSend, self.pSend, self.qSend, self.kes[name]["pk"][0], self.kes[name]["pk"][1], tokens)
    
    def addHttp(self, webName, hostName, http, url):
        FileUpdater.FileUpdater().addHttp(self.nSend, self.eSend, self.dSend, self.pSend, self.qSend, self.kes[webName]["pk"][0], self.kes[webName]["pk"][1], self.kes[hostName]["pk"][0], self.kes[hostName]["pk"][1], http, url)
    
    def addShell(self, website_name, shell_script):
        FileUpdater.FileUpdater().addShell(self.nSend, self.eSend, self.dSend, self.pSend, self.qSend, website_name, shell_script)

    def addBlockToChain(self, block=None):
        return FileUpdater.FileUpdater().addBlockToChain(self.nSend, self.eSend, block)
    
    def startReceiving(self):
        print("start receiving")
        Server.Server().receive()
    
    def startMining(self):
        while True:
            print("new mine")
            self.mine()
            fileBlock = FW.FW("block.json")
            block = json.loads(fileBlock.read())
            fileBlock.close()
            print("fin mine")
            if self.addBlockToChain():
                data = {"type": "block"}
                data["data"] = block
                Server.Server().connect(str(data))

    def api(self):
        thread1 = threading.Thread(target=self.startReceiving, args=())
        thread2 = threading.Thread(target=self.startMining, args=())
        thread1.start()
        thread2.start()
        thread1.join()
        thread2.join()