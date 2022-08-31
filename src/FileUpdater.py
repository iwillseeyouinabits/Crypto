import json
import FW

class FileUpdater:

    def __init__(self, data):
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
        fileBlock.write(block)
        fileBlock.close()