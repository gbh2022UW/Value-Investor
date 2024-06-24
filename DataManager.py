import os
import csv

save_path = None
portfolio_save_path = None
symbol_save_path = None
session_save_path = None
symbols = {}
portfolios = {}
sessions = {}

data_template = {"EBIT" : None,
                 "Current Revenue" : None,
                 "Three Years Revenue" : None,
                 "Enterprise Value" : None,
                 "Return Enterprise Value" : None,
                 "Revenue Change" : None,
                 "EBIT Margin" : None}

def Quit():
    for session in sessions:
        session_path = os.path.join(session_save_path, session.name)
        data_path = os.path.join(session_path, "data.csv")
        data_csv = open(data_path, "w")
        fieldnames = {"Symbols"}
        data_writer = csv.DictWriter(data_csv, fieldnames)
        data_writer.writeheader()
        for symbol in session.symbols:
            data_writer.writerow(symbol.ticker_name)

    for portfolio in portfolios:
        portfolio_path = os.path.join(portfolio_save_path, portfolio.name)

        for stock in portfolio.stocks:
            stock_path = os.path.join(portfolio_path, stock.name)
            data_path = os.path.join(stock_path, "data.csv")
            data_csv = open(data_path, "w")
            fieldnames = {"Competitors"}
            data_writer = csv.DictWriter(data_csv, fieldnames)
            data_writer.writeheader()
            for competitor in stock.competitors:
                data_writer.writerow(competitor.ticker_name)
    
    for symbol in symbols:
        symbol_path = os.path.join(symbol_save_path, symbol.ticker_name)
        data_path = os.path.join(symbol_path, "data.csv")
        data_csv = open(data_path, "w")
        fieldnames = dict.fromkeys(data_template)
        data_writer = csv.DictWriter(data_csv, fieldnames)
        data_writer.writeheader()
        for row in data_writer:
            for data_value in row:
                row[data_value] = symbol.data[data_value]
