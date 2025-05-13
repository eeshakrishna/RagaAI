import yfinance as yf

class APIAgent:
    def __init__(self, ticker):
        self.ticker = ticker

    def get_data(self):
        stock = yf.Ticker(self.ticker)
        historical_data = stock.history(period="1d")
        return historical_data

# Example usage
if __name__ == "__main__":
    ticker_input = input("Enter a stock ticker (e.g., AAPL): ")
    agent = APIAgent(ticker_input)  # Get data for the entered stock ticker
    data = agent.get_data()
    print(data)
