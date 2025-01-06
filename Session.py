class Session:
    def __init__(self, name, 
                 shown_statistics = ["Return Enterprise Value", 
                                     "Three Year Revenue Change", 
                                     "EBIT Margin", 
                                     "Debt/Equity", 
                                     "Sector", 
                                     "Industry"],
                   hidden_statistics = [], symbols = None):
        self.name = name
        if(symbols != None):
            self.symbols = symbols
            self.hidden_statistics = hidden_statistics
            self.shown_statistics = shown_statistics
        else:
            self.symbols = {}
            self.hidden_statistics = hidden_statistics
            self.shown_statistics = shown_statistics

    def GetShownData(self, symbol):
        data = []
        for shown_statistic in self.shown_statistics:
            statistic = symbol.data[shown_statistic]
            
            if type(statistic) is not str:
                statistic = round(statistic, 2)
            
            data.append(statistic)
        return data