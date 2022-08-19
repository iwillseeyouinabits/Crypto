import portalocker

class FWS:
    def __init__(self):
        with portalocker.Lock("test.json") as fh:
            fh.write("test")