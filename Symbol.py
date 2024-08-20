import yfinance as yf

class Symbol:
    def __init__(self, ticker_name, data = None):
        self.ticker_name = ticker_name
        if data is None:
            print(ticker_name)
            try:
                self.ticker = yf.Ticker(ticker_name)

                try:
                    self.revenue_current = self.ticker.financials.loc["Total Revenue"][0]
                    self.revenue_three_years = self.ticker.financials.loc["Total Revenue"][3]
                    self.three_change_revenue = (self.revenue_current / self.revenue_three_years - 1) / 3 * 100

                except:
                    self.revenue_current = 0
                    self.revenue_three_years = 0
                    self.three_change_revenue = 0

                #not currently working, cant access past 3 years
                try:
                    self.five_change_revenue = (self.revenue_current / self.revenue_five_years - 1) / 5 * 100
                    self.ten_change_revenue = (self.revenue_current / self.revenue_ten_years - 1) / 10 * 100
                    self.revenue_five_years = self.ticker.financials.loc["Total Revenue"][5]
                    self.revenue_ten_years = self.ticker.financials.loc["Total Revenue"][10]
                except:
                    self.five_change_revenue = 0
                    self.ten_change_revenue = 0
                    self.revenue_five_years = 0
                    self.revenue_ten_years = 0

                try:
                    self.ebit = self.ticker.financials.loc["EBIT"][0]
                    self.ebit_margin = self.ebit / self.revenue_current * 100
                except:
                    self.ebit = 0
                    self.ebit_margin = 0
                try:
                    self.enterprise_value = self.ticker.info["enterpriseValue"]
                    self.return_enterprise_value = self.ebit / self.enterprise_value * 100
                except:
                    self.enterprise_value = 0
                    self.return_enterprise_value = 0

                try:
                    self.debt_to_equity = self.ticker.info["debtToEquity"]
                except:
                    self.debt_to_equity = 0
                
                print(self.ticker.info)
                
                
                self.data = {"EBIT" : self.ebit,
                     "Current Revenue" : self.revenue_current,
                     "Three Years Revenue" : self.revenue_three_years,
                     "Five Years Revenue" : self.revenue_five_years,
                     "Ten Years Reveneue" : self.revenue_ten_years,
                     "Enterprise Value" : self.enterprise_value,
                     "Return Enterprise Value" : self.return_enterprise_value,
                     "Three Year Revenue Change" : self.three_change_revenue,
                     "Five Year Revenue Change" : self.five_change_revenue,
                     "Ten Year Revenue Change" : self.ten_change_revenue,
                     "EBIT Margin" : self.ebit_margin,
                     "Debt/Equity" : self.debt_to_equity}
            except:
                self.data = {"EBIT" : 0,
                     "Current Revenue" : 0,
                     "Three Years Revenue" : 0,
                     "Five Years Revenue" : 0,
                     "Ten Years Revenue" : 0,
                     "Enterprise Value" : 0,
                     "Return Enterprise Value" : 0,
                     "Three Year Revenue Change" : 0,
                     "Five Year Revenue Change" : 0,
                     "Ten Year Revenue Change" : 0,
                     "EBIT Margin" : 0,
                     "Debt/Equity" : 0}
            
        else:
            self.data = data    
        
    
    

    
    

    

