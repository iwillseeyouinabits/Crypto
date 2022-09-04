import json
import time
import random
import FW
import base64
import hashlib
import rsa
from Verify import Verify

class FileUpdater:

    def __init__(self, data="{\"type\":\"none\"}"):
        data = json.loads(data)
        if data["type"] == "block":
            self.block(data["data"])
        elif data["type"] == "currency":
            self.currency(data["type"])
        elif data["type"] == "http":
            self.http(data["data"])
        elif data["type"] == "shell":
            self.shell(data["data"])
    
    def block(self, data):
        fileBlockChain = FW.FW("blockchain.json")
        fileBlock = FW.FW("block.json")
        blockchain = json.loads(fileBlockChain.read())
        blockchain.update(data)
        fileBlockChain.write(blockchain)
        fileBlock.write("") #update this with empty block string
        fileBlock.close()
        fileBlockChain.close()

    def currency(self, data):
        fileBlock = FW.FW("block.json")
        block = json.loads(fileBlock.read())
        block["block"]["currency"].update(data)
        fileBlock.write(block)
        fileBlock.close()

    def http(self, data):
        fileBlock = FW.FW("block.json")
        block = json.loads(fileBlock.read())
        block["block"]["http"].update(data)
        fileBlock.write(block)
        fileBlock.close()

    def shell(self, data):
        fileBlock = FW.FW("block.json")
        block = json.loads(fileBlock.read())
        block["block"]["shell"].update(data)
        fileBlock.write(json.dumps(block, indent=4))
        fileBlock.close()

    def updateBlock(self):
        fileBlock = FW.FW("block.json")
        block = json.loads(fileBlock.read())
        block["block"]["timestamp"] = int(time.time())
        block["block"]["nonce"] = random.randrange(1000000)
        block["block_hash"] = hashlib.sha256(str(block["block"]).encode('utf-8')).hexdigest()
        print(json.dumps(block, indent=4))
        fileBlock.write(json.dumps(block, indent=4))
        fileBlock.close()

    def mine(self, numZeros):
        while True:
            self.updateBlock()
            fileBlock = FW.FW("block.json") 
            block = json.loads(fileBlock.read())
            if(block["block_hash"][:numZeros] == numZeros*"0"):
                break
            fileBlock.close()

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
        self.updateBlock()

    def addBlockToChain(self, selfN, selfE, block=None):
        if block == None:
            fileBlock = FW.FW("block.json")
            block = json.loads(fileBlock.read())
            fileBlock.close()
        if Verify().verify(block):
            fileBlockChain = FW.FW("blockChain.json")
            blockChain = json.loads(fileBlockChain.read())
            blockChain.append(block)
            fileBlockChain.write(json.dumps(blockChain, indent=4))
            fileBlockChain.close()
            self.makeNewBlock(selfN, selfE)