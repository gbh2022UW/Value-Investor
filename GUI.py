import PySimpleGUI as sg
sg.theme("DarkPurple5")
import DataManager as DM
import Session
import Portfolio
import Symbol
import Stock
import os
import shutil
import yfinance as yf
import pandas as pd

'''
class GUI:
    def __init__(self):
        self.windows = {}
        self.windows["Welcome"] = WelcomeTemplate(self)
        self.windowStack = []
        self.activeWindow = None
    
    def SwitchWindow(self, newWindow, closePrevious = True):
        if not self.activeWindow == None:
            self.windowStack.append(self.activeWindow)
            if closePrevious:
                self.activeWindow.close()
        self.activeWindow = self.windows[newWindow] 
        self.activeWindow.Activate()
        
    def GoBack(self):
        if len(self.windowStack) > 0:
            nextWindow = self.windowStack[-1]
            self.windowStack.pop()
            self.SwitchWindow(nextWindow)
'''
    
    
def WelcomeTemplate():
    session_names = []
    for session in DM.sessions:
        session_names.append(session)
    portfolio_names = []
    for portfolio in DM.portfolios:
        portfolio_names.append(portfolio)
    layout = [
        [sg.Text("Welcome to Value Investor!", font = ("Times New Roman", 24))],
        [sg.Button("Load Stock Research Session", key = "??LOAD SESSION??"), sg.Combo(session_names, s = (40, 50), key = "??LOAD SESSION NAME??")],
        [sg.Button("New Stock Research Session", key = "??NEW SESSION??"), sg.Input(key = "??NEW SESSION NAME??")],
        [sg.Button("Delete Session", key="??DELETE SESSION??"), sg.Combo(session_names, key="??DELETE SESSION NAME??")],
        [sg.Button("Quit", key = "??QUIT??")]
        
    ]
    window = sg.Window("Value Investor", layout)
    return window

def StockResearchTemplate(session_name):
    headings = DM.sessions[session_name].shown_statistics
    treedata = sg.TreeData()
    for symbol in DM.sessions[session_name].symbols.values():
        key = "??" + symbol.ticker_name + "??"
        treedata.Insert("", key, symbol.ticker_name, DM.sessions[session_name].GetShownData(symbol))
    symbols = []
    for symbol in DM.sessions[session_name].symbols:
        symbols.append(symbol)
    layout = [
        [sg.Text(session_name, font = ("Times New Roman", 24))],
        [sg.Button("Home", key = "??HOME??")],
        [sg.Button("Add Symbol", key = "??ADD SYMBOL??"), sg.Input(default_text="name", key = "??ADD SYMBOL NAME??"), sg.Button("Refresh", key = "??REFRESH??")],
        [sg.Tree(treedata, headings = headings, enable_events = True, change_submits = True, key  = "??TREE??")],
        [sg.Button("Delete Symbol", key = "??DELETE SYMBOL??"), sg.Combo(symbols, key = "??DELETE SYMBOL NAME??"), 
         sg.Button("Hide Statistic", key = "??HIDE STATISTIC??"), sg.Combo(DM.sessions[session_name].shown_statistics, key = "??HIDE STATISTIC NAME??"), 
         sg.Button("Show Statistic", key = "??SHOW STATISTIC??"), sg.Combo(DM.sessions[session_name].hidden_statistics, key = "??SHOW STATISTIC NAME??")],
        [sg.Button("Sort by Highest", key = "??SORT BY HIGHEST??"), sg.Button("Sort by Lowest", key = "??SORT BY LOWEST??"), sg.Combo(DM.sessions[session_name].shown_statistics, key = "??SORT STATISTIC NAME??")],
        [sg.Button("Update Data", key = "??UPDATE??")],
        [sg.Button("Extract Stocks", key = "??EXTRACT??"), sg.Input(key = "??EXTRACT SESSION NAME??", default_text="new session name"), sg.Combo(DM.sessions[session_name].shown_statistics, key = "??EXTRACT STATISTIC NAME??"), sg.Input(default_text="value/name used for extraction", key="??EXTRACT VALUE??"), sg.Checkbox("Extract Higher Than", default=True, key="??EXTRACT HIGHER/LOWER??")],
        [sg.Button("Purge By Statistic", key="??PURGE??"), sg.Combo(DM.sessions[session_name].shown_statistics, key="??PURGE STATISTIC NAME??"), sg.Input(default_text="value to purge higher/lower from", key="??PURGE VALUE??"), sg.Checkbox("Purge Higher Than", default=True, key="??PURGE HIGHER/LOWER??")],
        [sg.Button("Quit", key = "??QUIT??")]
        
    ]
    window = sg.Window("Value Investor", layout)
    return window

def MyPortfoliosTemplate(portfolio_name):
    stock_names = []
    for stock in DM.portfolios[portfolio_name].stocks.values():
        stock_names.append(stock.symbol.ticker_name)
    layout = [
        [sg.Text(portfolio_name, font = ("Times New Roman", 24))],
        [sg.Button("Home", key = "??HOME??")],
        [sg.Button("Add Stock", key = "??ADD STOCK??"), sg.Input(key = "??ADD STOCK NAME??")],
        [sg.Button("Add Competitor", key = "??ADD COMPETITOR??"), sg.Input(key = "??ADD COMPETITOR NAME??"), sg.Combo(stock_names, s = (40, 50), key = "??LOAD STOCK NAME??")],
        [sg.Button("Quit", key = "??QUIT??")]
        
    ]
    window = sg.Window("Value Investor", layout)
    return window

class Window():
    def __init__(self, window):
        self.window = window

    def Activate(self):
        self.next_window = None
        self.close = False
        while True:
            if self.close:
                break
            event, values = self.window.read()

            self.RunEvents(event, values)

            '''if event == "??Back??":
                self.parent.GoBack()'''
            if event == sg.WIN_CLOSED:
                DM.Quit()
                break
            if event == "??QUIT??":
                DM.Quit()
                break
        
        if not self.next_window is None:
            self.window.close()
            self.next_window.Activate()
            self.next_window = None

    def RunEvents(self, event, values):
        for function in self.eventFunctions:
            function(event, values)

#inherits window
class WelcomeWindow(Window):
    def __init__(self, window):
        self.window = window
        self.eventFunctions = [self.WelcomeEvents]

    def WelcomeEvents(self, event, values):
        if event == "??LOAD SESSION??":
            self.next_window = StockResearchWindow(StockResearchTemplate(values["??LOAD SESSION NAME??"]), values["??LOAD SESSION NAME??"])
            self.close = True
        if event == "??NEW SESSION??":
            new_session_name = values["??NEW SESSION NAME??"]
            if new_session_name == "":
                if DM.new_session_count == 0:
                    new_session_name = "New Session"
                else:
                    new_session_name = "New Session " + str(DM.new_session_count)
            DM.sessions[new_session_name] = Session.Session(new_session_name)
            self.next_window = StockResearchWindow(StockResearchTemplate(new_session_name), new_session_name)
            self.close = True
        if event == "??LOAD PORTFOLIO??":
            self.next_window = MyPortfoliosWindow(MyPortfoliosTemplate(values["??LOAD PORTFOLIO NAME??"]), values["??LOAD PORTFOLIO NAME??"])
            self.close = True
        if event == "??NEW PORTFOLIO??":
            new_portfolio_name = values["??NEW PORTFOLIO NAME??"]
            if new_portfolio_name == "":
                if DM.new_portfolio_count == 0:
                    new_portfolio_name = "New Portfolio"
                else:
                    new_portfolio_name = "New Portfolio " + str(DM.new_portfolio_count)
            DM.portfolios[new_portfolio_name] = Portfolio.Portfolio(new_portfolio_name)
            self.next_window = MyPortfoliosWindow(MyPortfoliosTemplate(new_portfolio_name), new_portfolio_name)
            self.close = True

        if event == "??DELETE SESSION??":
            del DM.sessions[values["??DELETE SESSION NAME??"]]
            shutil.rmtree(os.path.join(DM.session_save_path, values["??DELETE SESSION NAME??"]))

    
    
#inherits the window class
class StockResearchWindow(Window):
    def __init__(self, window, session_name):
        self.window = window
        self.session_name = session_name
        self.eventFunctions = [self.StockResearchEvents]

    def StockResearchEvents(self, event, values):
        if event == "??HOME??":
            self.next_window = WelcomeWindow(WelcomeTemplate())
            self.close = True
        if event == "??ADD SYMBOL??" and values["??ADD SYMBOL NAME??"] == "FULLLIST":
            snp500_table = pd.read_html('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies'
)
            snp500_df = snp500_table[0]
            tickers = snp500_df["Symbol"].tolist()

            for name in tickers:
                if not name in DM.symbols:
                    new_symbol = Symbol.Symbol(name)
                    DM.symbols[name] = new_symbol
                else:
                    new_symbol = DM.symbols[name]
                DM.sessions[self.session_name].symbols[name] = new_symbol

        if event == "??ADD SYMBOL??" and values["??ADD SYMBOL NAME??"] == "FULL3000":
            
            for name in tickers:
                if not name in DM.symbols:
                    new_symbol = Symbol.Symbol(name)
                    DM.symbols[name] = new_symbol
                else:
                    new_symbol = DM.symbols[name]
                DM.sessions[self.session_name].symbols[name] = new_symbol

        elif event == "??ADD SYMBOL??":
            new_symbol_name = values["??ADD SYMBOL NAME??"]
            if not new_symbol_name in DM.symbols:
                new_symbol = Symbol.Symbol(new_symbol_name)
                DM.symbols[new_symbol_name] = new_symbol
            else:
                new_symbol = DM.symbols[new_symbol_name]
            DM.sessions[self.session_name].symbols[new_symbol_name] = new_symbol
        if event == "??REFRESH??":
            self.next_window = StockResearchWindow(StockResearchTemplate(self.session_name), self.session_name)
            self.close = True
        if event == "??DELETE SYMBOL??":
            delete_symbol = values["??DELETE SYMBOL NAME??"]
            if delete_symbol in DM.sessions[self.session_name].symbols:
                DM.sessions[self.session_name].symbols.pop(delete_symbol)
        #in progress
        if event == "??UPDATE??":
            #shutil.rmtree(DM.symbol_save_path)
            for symbol in DM.sessions[self.session_name].symbols:
                DM.symbols[symbol] = Symbol.Symbol(symbol)
            #add loading bar / screen
        
        if event == "??HIDE STATISTIC??":
            if values["??HIDE STATISTIC NAME??"] in DM.sessions[self.session_name].shown_statistics:
                DM.sessions[self.session_name].shown_statistics.remove(values["??HIDE STATISTIC NAME??"])
                DM.sessions[self.session_name].hidden_statistics.append(values["??HIDE STATISTIC NAME??"])
            else:
                pass
        if event == "??SHOW STATISTIC??":
            if values["??SHOW STATISTIC NAME??"] in DM.sessions[self.session_name].hidden_statistics:
                DM.sessions[self.session_name].hidden_statistics.remove(values["??SHOW STATISTIC NAME??"])
                DM.sessions[self.session_name].shown_statistics.append(values["??SHOW STATISTIC NAME??"])
            else:
                pass

        if event == "??SORT BY LOWEST??":
            if values["??SORT STATISTIC NAME??"] != "":
                data = {}
                for symbol in DM.sessions[self.session_name].symbols:
                    data[symbol] = DM.sessions[self.session_name].symbols[symbol].data[values["??SORT STATISTIC NAME??"]]
                data = dict(sorted(data.items(), key=lambda item: item[1]))

                temp_symbols = DM.sessions[self.session_name].symbols
                DM.sessions[self.session_name].symbols = {}
                for symbol in data:
                    DM.sessions[self.session_name].symbols[symbol] = temp_symbols[symbol]
        if event == "??SORT BY HIGHEST??":
            if values["??SORT STATISTIC NAME??"] != "":
                data = {}
                for symbol in DM.sessions[self.session_name].symbols:
                    data[symbol] = DM.sessions[self.session_name].symbols[symbol].data[values["??SORT STATISTIC NAME??"]]
                data = dict(sorted(data.items(), reverse=True, key=lambda item: item[1]))

                temp_symbols = DM.sessions[self.session_name].symbols
                DM.sessions[self.session_name].symbols = {}
                for symbol in data:
                    DM.sessions[self.session_name].symbols[symbol] = temp_symbols[symbol]

        if event == "??EXTRACT??":
            if values["??EXTRACT STATISTIC NAME??"] == "Industry" or values["??EXTRACT STATISTIC NAME??"] == "Sector":
                DM.sessions[values["??EXTRACT SESSION NAME??"]] = Session.Session(name=values["??EXTRACT SESSION NAME??"])
                for symbol in DM.sessions[self.session_name].symbols:
                    if DM.symbols[symbol].data[values["??EXTRACT STATISTIC NAME??"]] == values["??EXTRACT VALUE??"]:
                        DM.sessions[values["??EXTRACT SESSION NAME??"]].symbols[symbol] = DM.symbols[symbol]
            else:
                DM.sessions[values["??EXTRACT SESSION NAME??"]] = Session.Session(name=values["??EXTRACT SESSION NAME??"])
                for symbol in DM.sessions[self.session_name].symbols:
                    if values["??EXTRACT HIGHER/LOWER??"]:
                        if DM.symbols[symbol].data[values["??EXTRACT STATISTIC NAME??"]] > float(values["??EXTRACT VALUE??"]):
                            DM.sessions[values["??EXTRACT SESSION NAME??"]].symbols[symbol] = DM.symbols[symbol]
                    else:
                        if DM.symbols[symbol].data[values["??EXTRACT STATISTIC NAME??"]] <= float(values["??EXTRACT VALUE??"]):
                            DM.sessions[values["??EXTRACT SESSION NAME??"]].symbols[symbol] = DM.symbols[symbol]
        
        if event == "??PURGE??":
            deletes = []
            for symbol in DM.sessions[self.session_name].symbols:
                if values["??PURGE HIGHER/LOWER??"]:
                    if DM.symbols[symbol].data[values["??PURGE STATISTIC NAME??"]] > float(values["??PURGE VALUE??"]):
                        deletes.append(DM.sessions[self.session_name].symbols[symbol].ticker_name)
                else:
                    if DM.symbols[symbol].data[values["??PURGE STATISTIC NAME??"]] <= float(values["??PURGE VALUE??"]):
                        deletes.append(DM.sessions[self.session_name].symbols[symbol].ticker_name)
            for delete in deletes:
                del DM.sessions[self.session_name].symbols[delete]

            


class MyPortfoliosWindow(Window):
    def __init__(self, window, portfolio_name):
        self.window = window
        self.portfolio_name = portfolio_name
        self.eventFunctions = [self.MyPortfoliosEvents]

    def MyPortfoliosEvents(self, event, values):
        if event == "??ADD STOCK??":
            new_stock_name = values["??ADD STOCK NAME??"]
            DM.portfolios[self.portfolio_name].stocks[new_stock_name] = Stock.Stock(DM.symbols[new_stock_name])
        if event == "??ADD COMPETITOR??":
            new_competitor_name = values["??ADD COMPETITOR NAME??"]
            load_stock_name = values["??LOAD STOCK NAME??"]
            if not new_competitor_name in DM.symbols:
                DM.symbols[new_competitor_name] = Symbol.Symbol(new_competitor_name)
            DM.portfolios[self.portfolio_name].stocks[load_stock_name].competitors[new_competitor_name] = DM.symbols[new_competitor_name]
        if event == "??HOME??":
            self.next_window = WelcomeWindow(WelcomeTemplate())
            self.close = True
