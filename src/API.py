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
        self.pk = kes[name]["pk"]
        self.sk = kes[name]["sk"]
        self.kes = kes

    def mine(self, numZeros=4):
        FileUpdater.FileUpdater().mine(numZeros, self.pk)
    
    def addCurrency(self, name, tokens):
        FileUpdater.FileUpdater().addCurrency(self.pk, self.sk, self.kes[name]["pk"], tokens)
    
    def addHttp(self, webName, hostName, http, url):
        FileUpdater.FileUpdater().addHttp(self.pk, self.sk, self.kes[webName]["pk"], self.kes[hostName]["pk"], http, url)
    
    def addShell(self, website_name, shell_script):
        FileUpdater.FileUpdater().addShell(self.pk, self.sk, website_name, shell_script)

    def addBlockToChain(self, block=None):
        return FileUpdater.FileUpdater().addBlockToChain(self.pk, block)
    
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