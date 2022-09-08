import portalocker

class FW:
    def __init__(self, fileName):
        file = open(fileName, "+r")
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
                fileText = self.file.read()
                self.file.seek(0)
                return fileText
            except Exception as e:
                print(e)
    
    def close(self):
        portalocker.unlock(self.file)
        self.file.close()