from email import message
import hashlib
import json
import time
import rsa
import FW

class Verify:
    def hash(self, hash, message):
        hash2 = hashlib.sha256(str(message).encode('utf-8')).hexdigest()
        if hash == hash2:
            return True
        return False

    def blockHeight(self):
        blockChainFile = FW.FW("blockChain.json")
        blockChain = json.loads(blockChainFile.read())
        blockChainFile.close()
        length = len(blockChain)
        return length

    def previouseBlockHash(self, hash):
        blockChainFile = FW.FW("blockChain.json")
        blockChain = json.loads(blockChainFile.read())
        blockChainFile.close()
        if len(blockChain) > 0:
            previoseBlockHash = blockChain[len(blockChain)-1]["previous_block_hash"]
            if previoseBlockHash == hash:
                return True
            return False
        return True

    def timeStamp(self, stamp):
        blockChainFile = FW.FW("blockChain.json")
        blockChain = json.loads(blockChainFile.read())
        blockChainFile.close()
        if len(blockChain) > 0:
            stamp2 = blockChain[len(blockChain)-1]["block"]["timestamp"]
            if stamp2 < stamp < int(time.time()):
                return True
            return False
        return True
    
    def quantifyBlockChainCashTotal(self): 
        blockChainFile = FW.FW("blockChain.json")
        blockChain = json.loads(blockChainFile.read())
        blockChainFile.close()
        cashSums = {}
        try:
            for block in blockChain[1:]:
                wallet = 0
                if block["block"]["minner_address"] in cashSums:
                    wallet += block["block"]["minner_address"]
                wallet += 50000
                cashSums[block["block"]["minner_address"]] = wallet
                for transaction in block["block"]["currency"]:
                    wallet = 0
                    if transaction["transaction_body"]["sender_adress"] in cashSums:
                        wallet += cashSums[transaction["transaction_body"]["sender_adress"]]
                    wallet -= transaction["base_fee"] + transaction["gass_fee"] + transaction["transaction_body"]["tokens"]
                    cashSums[transaction["transaction_body"]["sender_adress"]] = wallet
                    wallet = 0
                    if transaction["transaction_body"]["recipient_adress"] in cashSums:
                        wallet += cashSums[transaction["transaction_body"]["recipient_adress"]]
                    wallet += transaction["transaction_body"]["tokens"]
                    cashSums[transaction["transaction_body"]["recipient_adress"]] = wallet
                for transaction in block["block"]["http"]:
                    wallet = 0
                    if transaction["http_body"]["client_adress"] in cashSums:
                        wallet += cashSums[transaction["http_body"]["client_adress"]]
                    wallet -= transaction["base_fee"] + transaction["gass_fee"]
                    cashSums[transaction["http_body"]["client_adress"]] = wallet
                for transaction in block["block"]["shell"]:
                    wallet = 0
                    if transaction["shell_body"]["website_adress"] in cashSums:
                        wallet += cashSums[transaction["shell_body"]["website_adress"]]
                    wallet -= transaction["base_fee"] + transaction["gass_fee"]
                    cashSums[transaction["shell_body"]["website_adress"]] = wallet
            return cashSums
        except:
            print("first block")
            return cashSums

    def signature(self, signature, message, pk):
        try:
            rsa.verify(message.encode('utf-8'), signature, pk)
            return True
        except Exception as e:
            print(e)
            return False

    def gassFee(self, message, gass):
        if gass == (len(message) / (2**30))*10:
            return True
        return False
    
    def currency(self, transaction, cashSums):
        wallet = 0
        if transaction["transaction_body"]["sender_adress"] in cashSums:
            wallet += cashSums[transaction["transaction_body"]["sender_adress"]]
        wallet -= transaction["base_fee"] + transaction["gass_fee"] + transaction["transaction_body"]["tokens"]
        if wallet < 0 or transaction["transaction_body"]["tokens"] < 0:
            return False
        cashSums[transaction["transaction_body"]["sender_adress"]] = wallet
        wallet = 0
        if transaction["transaction_body"]["recipient_adress"] in cashSums:
            wallet += cashSums[transaction["transaction_body"]["recipient_adress"]]
        wallet += transaction["transaction_body"]["tokens"]
        if wallet < 0:
            return False
        cashSums[transaction["transaction_body"]["recipient_adress"]] = wallet
        if not self.hash(transaction["transaction_hash"], transaction["transaction_body"]):
            return False
        if not self.signature(transaction["transaction_signature"], transaction["transaction_body"], rsa.PublicKey.load_pkcs1_openssl_der(transaction["transaction_body"]["sender_adress"].encode('utf-8'))):
            return False
        if not (transaction["base_fee"] == 0.0025 or self.gassFee(transaction["transaction_body"], transaction["gass_fee"])):
            return False
        return True

    def http(self, transaction, cashSums):
        wallet = 0
        if transaction["http_body"]["client_adress"] in cashSums:
            wallet += cashSums[transaction["http_body"]["client_adress"]]
        wallet -= transaction["base_fee"] + transaction["gass_fee"]
        if wallet < 0:
            return False
        cashSums[transaction["http_body"]["client_adress"]] = wallet
        if not self.hash(transaction["http_hash"], transaction["http_body"]):
            return False
        if not self.signature(transaction["http_signature"], transaction["http_body"], rsa.PublicKey.load_pkcs1_openssl_der(transaction["http_body"]["client_adress"].encode('utf-8'))):
            return False
        if not (transaction["base_fee"] == 0.0025 or self.gassFee(transaction["http_body"], transaction["gass_fee"])):
            return False
        return True

    def shell(self, transaction, cashSums):
        wallet = 0
        if transaction["shell_body"]["website_adress"] in cashSums:
            wallet += cashSums[transaction["shell_body"]["website_adress"]]
        wallet -= transaction["base_fee"] + transaction["gass_fee"]
        if wallet < 0:
            return False
        cashSums[transaction["shell_body"]["website_adress"]] = wallet
        if not self.hash(transaction["shell_hash"], transaction["shell_body"]):
            return False
        if not self.signature(transaction["shell_signature"], transaction["shell_body"], rsa.PublicKey.load_pkcs1_openssl_der(transaction["shell_body"]["website_adress"].encode('utf-8'))):
            return False
        if not (transaction["base_fee"] == 0.0025 or self.gassFee(transaction["shell_body"], transaction["gass_fee"])):
            return False
        return True

    def verify(self):
        blockFile = FW.FW("block.json")
        block = json.loads(blockFile.read())
        blockFile.close()
        if not self.hash(block["block_hash"], block["block"]):
            return False
        if not self.blockHeight(block["block"]["block_height"]):
            return False
        if not self.previouseBlockHash(block["block"]["previous_block_hash"]):
            return False
        if not self.timeStamp(block["block"]["timestamp"]):
            return False
        cashSums = self.quantifyBlockChainCashTotal()
        for transaction in block["block"]["currency"]:
            if not self.currency(transaction, cashSums):
                return False
        for transaction in block["block"]["http"]:
            if not self.http(transaction, cashSums):
                return False
        for transaction in block["block"]["shell"]:
            if not self.shell(transaction, cashSums):
                return False
        return False
