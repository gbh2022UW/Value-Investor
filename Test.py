import yfinance as yf

amzn = yf.Ticker("BAYRY")

ebit = amzn.financials.loc["EBIT"][0]
revenue_current = amzn.financials.loc["Total Revenue"][0]
revenue_three_years = amzn.financials.loc["Total Revenue"][3]
enterprise_value = amzn.info["enterpriseValue"]

return_enterprise_value = ebit / enterprise_value * 100
change_revenue = (revenue_current / revenue_three_years - 1) / 3 * 100
ebit_margin = ebit / revenue_current * 100
print(return_enterprise_value)
print(change_revenue)
print(ebit_margin)
