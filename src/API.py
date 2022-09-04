import FileUpdater
import Server
import Verify
import threading

class API:
    def __init__(self, nSend, eSend, dSend, pSend, qSend):
        self.nSend = nSend
        self.eSend = eSend
        self.dSend = dSend
        self.pSend = pSend
        self.qSend = qSend

    def mine(self, numZeros=4):
        FileUpdater.FileUpdater().mine(numZeros)
    
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
    
    def startMining(self):
        while True:
            self.mine()
            if self.addBlockToChain():
                fileBlock = FW.FW("block.json")
                block = json.loads(fileBlock.read())
                fileBlock.close()
                data = {"type": "block"}
                data["data"] = block
                Server().connect(str(data))