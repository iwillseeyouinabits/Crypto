import json
import time
import random
import FW
import hashlib

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

