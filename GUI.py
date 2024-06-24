import PySimpleGUI as sg
sg.theme("DarkPurple5")
import DataManager as DM
import Session
import Portfolio

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
        [sg.Button("Load Portfolio", key = "??LOAD PORTFOLIO??"), sg.Combo(portfolio_names, s = (40, 50), key = "??LOAD PORTFOLIO NAME??")],
        [sg.Button("New Portfolio", key = "??NEW PORTFOLIO??"), sg.Input(key = "??NEW PORTFOLIO NAME??")],
        [sg.Button("Quit", key = "??QUIT??")]
        
    ]
    window = sg.Window("Value Investor", layout)
    return window

def StockResearchTemplate(session_name):
    layout = [
        [sg.Text(session_name, font = ("Times New Roman", 24))],
        [sg.Button("Home", key = "??HOME??")],
        [sg.Button("My Portfolios", key = "??MY PORTFOLIOS??")],
        [sg.Button("Quit", key = "??QUIT??")]
        
    ]
    window = sg.Window("Value Investor", layout)
    return window

def MyPortfoliosTemplate(portfolio_name):
    layout = [
        [sg.Text(portfolio_name, font = ("Times New Roman", 24))],
        [sg.Button("Home", key = "??HOME??")],
        [sg.Button("Stock Research", key = "??STOCK RESEARCH??")],
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

class WelcomeWindow(Window):
    def __init__(self, window):
        self.window = window
        self.eventFunctions = [self.WelcomeEvents]

    def WelcomeEvents(self, event, values):
        if event == "??LOAD SESSION??":
            self.next_window = StockResearchWindow(StockResearchTemplate(values["??LOAD SESSION NAME??"]))
            self.close = True
        if event == "??NEW SESSION??":
            new_session_name = values["??NEW SESSION NAME??"]
            if new_session_name == "":
                if DM.new_session_count == 0:
                    new_session_name = "New Session"
                else:
                    new_session_name = "New Session " + str(DM.new_session_count)
            DM.sessions[new_session_name] = Session.Session(new_session_name)
            self.next_window = StockResearchWindow(StockResearchTemplate(new_session_name))
            self.close = True
        if event == "??LOAD PORTFOLIO??":
            self.next_window = MyPortfoliosWindow(MyPortfoliosTemplate(values["??LOAD PORTFOLIO NAME??"]))
            self.close = True
        if event == "??NEW PORTFOLIO??":
            new_portfolio_name = values["??NEW PORTFOLIO NAME??"]
            if new_portfolio_name == "":
                if DM.new_portfolio_count == 0:
                    new_portfolio_name = "New Portfolio"
                else:
                    new_portfolio_name = "New Portfolio " + str(DM.new_portfolio_count)
            DM.portfolios[new_portfolio_name] = Portfolio.Portfolio(new_portfolio_name)
            self.next_window = MyPortfoliosWindow(MyPortfoliosTemplate(new_portfolio_name))
            self.close = True
    
    

class StockResearchWindow(Window):
    def __init__(self, window):
        self.window = window
        self.eventFunctions = [self.StockResearchEvents]

    def StockResearchEvents(self, event, values):
        if event == "??HOME??":
            print("Home")
            self.next_window = WelcomeWindow(WelcomeTemplate())
            self.close = True
        if event == "??MY PORTFOLIOS??":
            print("My Portfolios")
            self.next_window = MyPortfoliosWindow(MyPortfoliosTemplate())
            self.close = True


class MyPortfoliosWindow(Window):
    def __init__(self, window):
        self.window = window
        self.eventFunctions = [self.MyPortfoliosEvents]

    def MyPortfoliosEvents(self, event, values):
        if event == "??STOCK RESEARCH??":
            print("Stock Research")
            self.next_window = StockResearchWindow(StockResearchTemplate())
            self.close = True
        if event == "??HOME??":
            print("Home")
            self.next_window = WelcomeWindow(WelcomeTemplate())
            self.close = True
