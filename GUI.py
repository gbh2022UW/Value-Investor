import PySimpleGUI as sg
sg.theme("DarkPurple5")
import DataManager as DM

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
    layout = [
        [sg.Text("Welcome to Value Investor!", font = ("Times New Roman", 24))],
        [sg.Button("Stock Research", key = "??STOCK RESEARCH??")],
        [sg.Button("My Portfolios", key = "??MY PORTFOLIOS??")],
        [sg.Button("Quit", key = "??QUIT??")]
        
    ]
    window = sg.Window("Value Investor", layout)
    return window

def StockResearchTemplate():
    layout = [
        [sg.Text("Stock Research!", font = ("Times New Roman", 24))],
        [sg.Button("Home", key = "??HOME??")],
        [sg.Button("My Portfolios", key = "??MY PORTFOLIOS??")],
        [sg.Button("Quit", key = "??QUIT??")]
        
    ]
    window = sg.Window("Value Investor", layout)
    return window

def MyPortfoliosTemplate():
    layout = [
        [sg.Text("My Portfolios!", font = ("Times New Roman", 24))],
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
        self.eventFunctions = [self.StockResearchButton, self.MyPortfoliosButton]

    def StockResearchButton(self, event, values):
        if event == "??STOCK RESEARCH??":
            print("Stock Research")
            self.next_window = StockResearchWindow(StockResearchTemplate())
            self.close = True
    
    def MyPortfoliosButton(self, event, values):
        if event == "??MY PORTFOLIOS??":
            print("My Portfolios")
            self.next_window = MyPortfoliosWindow(MyPortfoliosTemplate())
            self.close = True

class StockResearchWindow(Window):
    def __init__(self, window):
        self.window = window
        self.eventFunctions = [self.HomeButton, self.MyPortfoliosButton]

    def HomeButton(self, event, values):
        if event == "??HOME??":
            print("Home")
            self.next_window = WelcomeWindow(WelcomeTemplate())
            self.close = True
    
    def MyPortfoliosButton(self, event, values):
        if event == "??MY PORTFOLIOS??":
            print("My Portfolios")
            self.next_window = MyPortfoliosWindow(MyPortfoliosTemplate())
            self.close = True


class MyPortfoliosWindow(Window):
    def __init__(self, window):
        self.window = window
        self.eventFunctions = [self.StockResearchButton, self.HomeButton]

    def StockResearchButton(self, event, values):
        if event == "??STOCK RESEARCH??":
            print("Stock Research")
            self.next_window = StockResearchWindow(StockResearchTemplate())
            self.close = True
    
    def HomeButton(self, event, values):
        if event == "??HOME??":
            print("Home")
            self.next_window = WelcomeWindow(WelcomeTemplate())
            self.close = True
