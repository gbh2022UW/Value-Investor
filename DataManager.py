import os
import csv

save_path = None
portfolio_save_path = None
symbol_save_path = None
session_save_path = None
symbols = {}
portfolios = {}
sessions = {}
new_session_count = 0
new_portfolio_count = 0

data_template = {"EBIT" : None,
                 "Current Revenue" : None,
                 "Three Years Revenue" : None,
                 "Enterprise Value" : None,
                 "Return Enterprise Value" : None,
                 "Revenue Change" : None,
                 "EBIT Margin" : None}

def Quit():
    for session in sessions.values():
        session_path = os.path.join(session_save_path, session.name)
        if not os.path.exists(session_path):
            os.mkdir(session_path)
        data_path = os.path.join(session_path, "data.csv")
        data_csv = open(data_path, "w")
        data_writer = csv.writer(data_csv)
        data_writer.writerow(session.symbols.keys())

    for portfolio in portfolios.values():
        portfolio_path = os.path.join(portfolio_save_path, portfolio.name)
        if not os.path.exists(portfolio_path):
            os.mkdir(portfolio_path)
        for stock in portfolio.stocks.values():
            stock_path = os.path.join(portfolio_path, stock.symbol.ticker_name)
            if not os.path.exists(stock_path):
                os.mkdir(stock_path)
            data_path = os.path.join(stock_path, "data.csv")
            data_csv = open(data_path, "w")
            data_writer = csv.writer(data_csv)
            records = [stock.symbol.ticker_name]
            for competitor in stock.competitors:
                records.append(competitor)
            data_writer.writerow(records)
    
    for symbol in symbols.values():
        symbol_path = os.path.join(symbol_save_path, symbol.ticker_name)
        if not os.path.exists(symbol_path):
            os.makedirs(symbol_path)
        data_path = os.path.join(symbol_path, "data.csv")
        data_csv = open(data_path, "w")
        fieldnames = dict.fromkeys(data_template)
        data_writer = csv.DictWriter(data_csv, fieldnames)
        data_writer.writeheader()
        data_writer.writerow(symbol.data)
