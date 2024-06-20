class Portfolio:
    def __init__(self, name, stocks = None):
        self.name = name
        if(stocks != None):
            self.stocks = stocks
        else:
            self.stocks = {}