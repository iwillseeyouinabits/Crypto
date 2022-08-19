import portalocker

class FW:
    def __init__(self, text, file):
        with portalocker.Lock(file) as fh:
            fh.write(text)