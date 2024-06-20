import os
import getpass
import DataManager as DM
import csv
import Symbol
import Stock
import Portfolio
import Session
import PySimpleGUI as sg

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
            data[data_value] = row[data_value]
    
    symbol = Symbol.Symbol(symbol_name, data)
    DM.symbols[symbol_name] = symbol

for portfolio_name in portfolio_names:
    portfolio_path = os.path.join(portfolio_save_path, portfolio_name)
    
    stock_save_path = os.path.join(portfolio_path, "Stocks")
    stock_names = os.listdir(stock_save_path)

    portfolio = Portfolio.Portfolio(portfolio_name)

    for stock_name in stock_names:
        stock_path = os.path.join(stock_save_path, stock_name)
        data_path = os.path.join(stock_path, "data.csv")
        data_csv = open(data_path, "r")
        data_reader = csv.DictReader(data_csv)
        competitors = []
        for row in data_reader:
            competitors.append(DM.symbols[row["Competitors"]])
        main_symbol = DM.symbols[stock_name]
        
        stock = Stock.Stock(main_symbol, competitors)
        portfolio.stocks[stock_name] = stock

    DM.portfolios[portfolio_name] = portfolio
        
for session_name in session_names:
    session_path = os.path.join(session_save_path, session_name)
    data_path = os.path.join(session_path, "data.csv")
    data_csv = open(data_path, "r")
    data_reader = csv.DictReader(data_csv)
    symbols = []
    for row in data_reader:
        symbols.append(DM.symbols[row["Symbols"]])
    
    session = Session.Session(session_name, symbols)
    DM.sessions[session_name] = session



