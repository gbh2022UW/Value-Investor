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
                    self.change_revenue = (self.revenue_current / self.revenue_three_years - 1) / 3 * 100
                except:
                    self.revenue_current = 0
                    self.revenue_three_years = 0
                    self.change_revenue = 0

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
                
                
                
                self.data = {"EBIT" : self.ebit,
                     "Current Revenue" : self.revenue_current,
                     "Three Years Revenue" : self.revenue_three_years,
                     "Enterprise Value" : self.enterprise_value,
                     "Return Enterprise Value" : self.return_enterprise_value,
                     "Revenue Change" : self.change_revenue,
                     "EBIT Margin" : self.ebit_margin}
            except:
                self.data = {"EBIT" : 0,
                     "Current Revenue" : 0,
                     "Three Years Revenue" : 0,
                     "Enterprise Value" : 0,
                     "Return Enterprise Value" : 0,
                     "Revenue Change" : 0,
                     "EBIT Margin" : 0}
            
        else:
            self.data = data    
        
    
    

    
    

    

