import portalocker

class FW:
    def __init__(self, file):
        file = open(file, "w+")
        portalocker.lock(file)
        self.file = file
    
    def write(self, text):
        while True:
            try:
                self.file.write(text)
            except Exception as e:
                print(e)
    
    
    def read(self):
        while True:
            try:
                return self.file.read()
            except Exception as e:
                print(e)
    
    def close(self):
        portalocker.unlock(self.file)
        self.file.close()