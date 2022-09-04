import FileUpdater
import Verify

class API:
    def __init__(self, nSend, eSend, dSend, pSend, qSend):
        self.nSend = nSend
        self.eSend = eSend
        self.dSend = dSend
        self.pSend = pSend
        self.qSend = qSend

    def mine(self, numZeros=3):
        FileUpdater.FileUpdater().mine(numZeros)
    
    def addCurrency(self, nReceive, eReceive, tokens):
        FileUpdater.FileUpdater().addCurrency(self.nSend, self.eSend, self.dSend, self.pSend, self.qSend, nReceive, eReceive, tokens)
    
    def addHttp(self, nWebsite, eWebsite, nHost, eHost, http, url):
        FileUpdater.FileUpdater().addHttp(self.nSend, self.eSend, self.dSend, self.pSend, self.qSend, nWebsite, eWebsite, nHost, eHost, http, url)
    
    def addShell(self, website_name, shell_script):
        FileUpdater.FileUpdater().addShell(self.nSend, self.eSend, self.dSend, self.pSend, self.qSend, website_name, shell_script)

    def addBlockToChain(self, block=None):
        FileUpdater.FileUpdater().addBlockToChain(self.nSend, self.eSend, block)