class Session:
    def __init__(self, name, symbols = None):
        self.name = name
        if(symbols != None):
            self.symbols = symbols
        else:
            self.symbols = {}