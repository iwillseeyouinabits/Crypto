import FileUpdater
import Server
import json
import FW
import threading

class API:
    def __init__(self, nSend, eSend, dSend, pSend, qSend):
        self.nSend = nSend
        self.eSend = eSend
        self.dSend = dSend
        self.pSend = pSend
        self.qSend = qSend

    def mine(self, n, e, numZeros=4):
        FileUpdater.FileUpdater().mine(numZeros, n, e)
    
    def addCurrency(self, nReceive, eReceive, tokens):
        FileUpdater.FileUpdater().addCurrency(self.nSend, self.eSend, self.dSend, self.pSend, self.qSend, nReceive, eReceive, tokens)
    
    def addHttp(self, nWebsite, eWebsite, nHost, eHost, http, url):
        FileUpdater.FileUpdater().addHttp(self.nSend, self.eSend, self.dSend, self.pSend, self.qSend, nWebsite, eWebsite, nHost, eHost, http, url)
    
    def addShell(self, website_name, shell_script):
        FileUpdater.FileUpdater().addShell(self.nSend, self.eSend, self.dSend, self.pSend, self.qSend, website_name, shell_script)

    def addBlockToChain(self, block=None):
        return FileUpdater.FileUpdater().addBlockToChain(self.nSend, self.eSend, block)
    
    def startReceiving(self):
        Server.Server().receive()
    
    def startMining(self, n, e):
        while True:
            print("new mine")
            self.mine(n, e)
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