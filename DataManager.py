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
        fieldnames = {"Symbols"}
        data_writer = csv.DictWriter(data_csv, fieldnames)
        data_writer.writeheader()
        for symbol in session.symbols:
            data_writer.writerow(symbol.ticker_name)

    for portfolio in portfolios.values():
        portfolio_path = os.path.join(portfolio_save_path, portfolio.name)
        if not os.path.exists(portfolio_path):
            os.mkdir(portfolio_path)
        for stock in portfolio.stocks.values():
            stock_path = os.path.join(portfolio_path, stock.name)
            if not os.path.exists(stock_path):
                os.mkdir(stock_path)
            data_path = os.path.join(stock_path, "data.csv")
            data_csv = open(data_path, "w")
            fieldnames = {"Competitors"}
            data_writer = csv.DictWriter(data_csv, fieldnames)
            data_writer.writeheader()
            for competitor in stock.competitors.values():
                data_writer.writerow(competitor.ticker_name)
    
    for symbol in symbols.values():
        symbol_path = os.path.join(symbol_save_path, symbol.ticker_name)
        data_path = os.path.join(symbol_path, "data.csv")
        data_csv = open(data_path, "w")
        fieldnames = dict.fromkeys(data_template)
        data_writer = csv.DictWriter(data_csv, fieldnames)
        data_writer.writeheader()
        for row in data_writer:
            for data_value in row:
                row[data_value] = symbol.data[data_value]
