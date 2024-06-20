class Stock:
    def __init__(self, symbol, competitors = None):
        self.symbol  = symbol
        if competitors != None:
            self.competitors = competitors
        else:
            self.competitors = {}