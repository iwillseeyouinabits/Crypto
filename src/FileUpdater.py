import json
from re import T
import time
import random
import FW
import base64
import hashlib
import rsa
import Verify
import Server

class FileUpdater:


    def currency(self, data):
        fileBlock = FW.FW("block.json")
        block = json.loads(fileBlock.read())
        if not data in block["block"]["currency"]:
            block["block"]["currency"].append(data)
            fileBlock.write(json.dumps(block, indent=4))
            fileBlock.close()
            print("added currency :D")
            return True
        fileBlock.close()
        print("already have currency")
        return False

    def http(self, data):
        fileBlock = FW.FW("block.json")
        block = json.loads(fileBlock.read())
        if not data in block["block"]["http"]:
            block["block"]["http"].append(data)
            fileBlock.write(json.dumps(block, indent=4))
            fileBlock.close()
            print("added http :D")
            return True
        fileBlock.close()
        print("already have http :D")
        return False

    def shell(self, data):
        fileBlock = FW.FW("block.json")
        block = json.loads(fileBlock.read())
        if not data in block["block"]["shell"]:
            block["block"]["shell"].append(data)
            fileBlock.write(json.dumps(block, indent=4))
            fileBlock.close()
            print("added shell :D")
            return True
        fileBlock.close()
        print("already have shell :D")
        return False

    def updateBlock(self, n, e):
        fileBlockChain = FW.FW("blockChain.json")
        blockChain = json.loads(fileBlockChain.read())
        fileBlockChain.close()
        print("load blockchain")
        fileBlock = FW.FW("block.json")
        block = json.loads(fileBlock.read())
        print("load block")
        block["block"]["timestamp"] = int(time.time())
        block["block"]["minner_address"] = [n, e]
        block["block"]["nonce"] = random.randrange(1000000)
        block["block"]["block_height"] = len(blockChain)
        print("load block timestamp minner_address nonce and block_hight")
        if len(blockChain) > 0:
            block["block"]["previous_block_hash"] = blockChain[-1]["block_hash"]
        else:
            block["block"]["previous_block_hash"] = None
        print("load block prev_hash")
        block["block_hash"] = hashlib.sha256(str(block["block"]).encode('utf-8')).hexdigest()
        print("load block hash")
        fileBlock.write(json.dumps(block, indent=4))
        print("write block")
        fileBlock.close()
        print("close block FW")

    def mine(self, numZeros, n, e):
        while True:
            try:
                print("start update")
                self.updateBlock(n, e)
                print("fin update")
                fileBlock = FW.FW("block.json") 
                block = json.loads(fileBlock.read())
                if(block["block_hash"][:numZeros] == numZeros*"0"):
                    break
                fileBlock.close()
            except:
                print("mine skiped for one nounce")

    def addCurrency(self, nSend, eSend, dSend, pSend, qSend, nReceive, eReceive, tokens):
        fileBlock = FW.FW("block.json")
        block = json.loads(fileBlock.read())
        trans = {}
        transBody = {}
        transBody["sender_adress"] = [nSend, eSend]
        transBody["recipient_adress"] = [nReceive, eReceive]
        transBody["tokens"] = tokens
        trans["transaction_body"] = transBody
        trans["transaction_hash"] = hashlib.sha256(str(transBody).encode('utf-8')).hexdigest()
        trans["base_fee"] = 0.0025
        trans["gass_fee"] = len(transBody)*10/(2**30)
        sig = rsa.sign(json.dumps(transBody).encode("utf-8"), rsa.PrivateKey(nSend, eSend, dSend, pSend, qSend), "SHA-256")
        trans["transaction_signature"] = base64.b64encode(sig).decode("ascii")
        block["block"]["currency"].append(trans)
        package = {"type": "currency"}
        package["data"] = trans
        Server.Server().connect(json.dumps(package))
        print(json.dumps(block, indent=4))
        fileBlock.write(json.dumps(block, indent=4))
        fileBlock.close()

    def addHttp(self, nSend, eSend, dSend, pSend, qSend, nWebsite, eWebsite, nHost, eHost, http, url):
        fileBlock = FW.FW("block.json")
        block = json.loads(fileBlock.read())
        trans = {}
        transBody = {}
        transBody["client_adress"] = [nSend, eSend]
        transBody["website_adress"] = [nWebsite, eWebsite]
        transBody["host_adress"] = [nHost, nHost]
        transBody["http_request"] = http
        transBody["host_URL"] = url
        trans["http_body"] = transBody
        trans["http_hash"] = hashlib.sha256(str(transBody).encode('utf-8')).hexdigest()
        trans["base_fee"] = 0.0025
        trans["gass_fee"] = len(transBody)*10/(2**30)
        sig = rsa.sign(json.dumps(transBody).encode("utf-8"), rsa.PrivateKey(nSend, eSend, dSend, pSend, qSend), "SHA-256")
        trans["http_signature"] = base64.b64encode(sig).decode("ascii")
        block["block"]["http"].append(trans)
        package = {"type": "http"}
        package["data"] = trans
        Server.Server().connect(json.dumps(package))
        print(json.dumps(block, indent=4))
        fileBlock.write(json.dumps(block, indent=4))
        fileBlock.close()
        
        

    def addShell(self, nSend, eSend, dSend, pSend, qSend, website_name, shell_script):
        fileBlock = FW.FW("block.json")
        block = json.loads(fileBlock.read())
        trans = {}
        transBody = {}
        transBody["website_adress"] = [nSend, eSend]
        transBody["website_name"] = website_name
        transBody["shell_script"] = shell_script
        trans["shell_body"] = transBody
        trans["shell_hash"] = hashlib.sha256(str(transBody).encode('utf-8')).hexdigest()
        trans["base_fee"] = 0.0025
        trans["gass_fee"] = len(transBody)*10/(2**30)
        sig = rsa.sign(json.dumps(transBody).encode("utf-8"), rsa.PrivateKey(nSend, eSend, dSend, pSend, qSend), "SHA-256")
        trans["shell_signature"] = base64.b64encode(sig).decode("ascii")
        block["block"]["shell"].append(trans)
        package = {"type": "shell"}
        package["data"] = trans
        Server.Server().connect(json.dumps(package))
        print(json.dumps(block, indent=4))
        fileBlock.write(json.dumps(block, indent=4))
        fileBlock.close()

    def makeNewBlock(self, selfN, selfE):
        fileBlockChain = FW.FW("blockChain.json")
        blockChain = json.loads(fileBlockChain.read())
        fileBlockChain.close()
        wholeBlock = {}
        wholeBlock["block_hash"] = ""
        block = {}
        block["block_height"] = len(blockChain)
        try:
            block["previous_block_hash"] = blockChain[-1]["block_hash"]
        except:
            block["previous_block_hash"] = None
        block["minner_address"] = [selfN, selfE]
        block["timestamp"] = int(time.time())
        block["nonce"] = 0
        block["currency"] = []
        block["http"] = []
        block["shell"] = []
        wholeBlock["block"] = block
        fileBlock = FW.FW("block.json")
        fileBlock.write(json.dumps(wholeBlock, indent=4))
        fileBlock.close()
        self.updateBlock(selfN, selfE)

    def addBlockToChain(self, selfN, selfE, block=None):
        if block == None:
            fileBlock = FW.FW("block.json")
            block = json.loads(fileBlock.read())
            fileBlock.close()
        else:
            print("received new block")
        if Verify.Verify().verify(block):
            fileBlockChain = FW.FW("blockChain.json")
            blockChain = json.loads(fileBlockChain.read())
            blockChain.append(block)
            fileBlockChain.write(json.dumps(blockChain, indent=4))
            fileBlockChain.close()
            self.makeNewBlock(selfN, selfE)
            return True
        return False

    def handleNewInfo(self, selfN, selfE, data):
        cashSums = Verify.Verify().quantifyBlockChainCashTotal()
        if data["type"] == "block":
            if self.addBlockToChain(selfN, selfE, data["data"]):
                Server.Server().connect(json.dumps(data))
                print("added block")
                return True
        elif data["type"] == "currency":
            if Verify.Verify().currency(data["data"], cashSums):
                if self.currency(data["data"]):
                    Server.Server().connect(json.dumps(data))
                    print("added currency")
                    return True
        elif data["type"] == "http":
            if Verify.Verify().http(data["data"], cashSums):
                if self.http(data["data"]):
                    Server.Server().connect(json.dumps(data))
                    print("added http")
                    return True
        elif data["type"] == "shell":
            if Verify.Verify().shell(data["data"], cashSums):
                if self.shell(data["data"]):
                    Server.Server().connect(json.dumps(data))
                    print("added shell")
                    return True
        else:
            print("FAILED TO HAVE A 'type' FOR DATA")
            raise ValueError("FAILED TO HAVE A 'type' FOR DATA")
        return False
