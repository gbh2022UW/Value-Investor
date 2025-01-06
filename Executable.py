import os
import getpass
import DataManager as DM
import csv
import Symbol
import Stock
import Portfolio
import Session
import GUI

username = getpass.getuser()

save_path = os.path.join(os.path.join(r"C:\Users", username), "Value Investor Save Files")
if not os.path.exists(save_path):
    os.makedirs(save_path)
DM.save_path = save_path

portfolio_save_path = os.path.join(save_path, "Portfolios")
if not os.path.exists(portfolio_save_path):
    os.makedirs(portfolio_save_path)
DM.portfolio_save_path = portfolio_save_path

symbol_save_path = os.path.join(save_path, "Symbols")
if not os.path.exists(symbol_save_path):
    os.makedirs(symbol_save_path)
DM.symbol_save_path = symbol_save_path

session_save_path = os.path.join(save_path, "Sessions")
if not os.path.exists(session_save_path):
    os.makedirs(session_save_path)
DM.session_save_path = session_save_path

symbol_names = os.listdir(symbol_save_path)
portfolio_names = os.listdir(portfolio_save_path)
session_names = os.listdir(session_save_path)

for symbol_name in symbol_names:
    symbol_path = os.path.join(symbol_save_path, symbol_name)
    data_path = os.path.join(symbol_path, "data.csv")
    data_csv = open(data_path, "r")
    data_reader = csv.DictReader(data_csv)
    data = {}
    for row in data_reader:
        for data_value in row:
            try:
                data[data_value] = float(row[data_value])
            except:
                data[data_value] = row[data_value]
    
    symbol = Symbol.Symbol(symbol_name, data)
    DM.symbols[symbol_name] = symbol
    data_csv.close()

for portfolio_name in portfolio_names:
    portfolio_path = os.path.join(portfolio_save_path, portfolio_name)
    
    stock_names = os.listdir(portfolio_path)

    portfolio = Portfolio.Portfolio(portfolio_name)

    for stock_name in stock_names:
        stock_path = os.path.join(portfolio_path, stock_name)
        data_path = os.path.join(stock_path, "data.csv")
        data_csv = open(data_path, "r")
        data_reader = csv.reader(data_csv)
        competitors_list = data_reader.__next__()
        competitors = {}
        main_symbol = DM.symbols[competitors_list[0]]
        index = 1
        while index < len(competitors_list):
            competitor = competitors_list[index]
            competitors[competitor] = DM.symbols[competitor]
            index += 1
        
        
        stock = Stock.Stock(main_symbol, competitors)
        portfolio.stocks[stock_name] = stock

        data_csv.close()

    DM.portfolios[portfolio_name] = portfolio
        
for session_name in session_names:
    session_path = os.path.join(session_save_path, session_name)
    data_path = os.path.join(session_path, "data.csv")
    data_csv = open(data_path, "r")
    data_reader = csv.reader(data_csv)
    symbols = {}
    for row in data_reader:
        for value in row:
            symbols[value] = DM.symbols[value]
    
    session = Session.Session(session_name, symbols=symbols)
    DM.sessions[session_name] = session

    data_csv.close()

for session in DM.sessions.values():
    if "New Session" in session.name:
        DM.new_session_count += 1
for portfolio in DM.portfolios.values():
    if "New Portfolio" in portfolio.name:
        DM.new_portfolio_count += 1



welcome_window = GUI.WelcomeWindow(GUI.WelcomeTemplate())
welcome_window.Activate()


