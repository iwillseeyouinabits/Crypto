import portalocker

class FW:
    def __init__(self, file):
        file = open(file, "+r")
        portalocker.lock(file, portalocker.LockFlags.EXCLUSIVE)
        self.file = file
    
    def write(self, text):
        while True:
            try:
                self.file.truncate(0)
                self.file.seek(0)
                self.file.write(text)
                break
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