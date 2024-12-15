import yfinance as yf

def get_financial_data(ticker):
    stock = yf.Ticker(ticker)
    
    balance_sheet = stock.balance_sheet
    working_capital = (
        balance_sheet.loc['Current Assets'].iloc[0] - balance_sheet.loc['Current Liabilities'].iloc[0]
    )
    total_assets = balance_sheet.loc['Total Assets'].iloc[0]
    total_liabilities = balance_sheet.loc['Total Liabilities Net Minority Interest'].iloc[0]
    
    income_statement = stock.financials
    try:
        ebit = income_statement.loc['EBIT'].iloc[0]
    except KeyError:
        try:
            ebit = income_statement.loc['Operating Income'].iloc[0]
        except KeyError:
            ebit = income_statement.loc['EBITDA'].iloc[0]
    
    sales = income_statement.loc['Total Revenue'].iloc[0]
    
    retained_earnings = balance_sheet.loc['Retained Earnings'].iloc[0]

    market_cap = stock.info['marketCap']

    return {
        "working_capital": working_capital,
        "total_assets": total_assets,
        "retained_earnings": retained_earnings,
        "ebit": ebit,
        "market_value_equity": market_cap,
        "total_liabilities": total_liabilities,
        "sales": sales,
    }

def calculate_altman_z_score(data):
    z_score = (
        1.2 * (data['working_capital'] / data['total_assets']) +
        1.4 * (data['retained_earnings'] / data['total_assets']) +
        3.3 * (data['ebit'] / data['total_assets']) +
        0.6 * (data['market_value_equity'] / data['total_liabilities']) +
        1.0 * (data['sales'] / data['total_assets'])
    )
    return z_score

ticker = "NXTT"
data = get_financial_data(ticker)
z_score = calculate_altman_z_score(data)

print(z_score)