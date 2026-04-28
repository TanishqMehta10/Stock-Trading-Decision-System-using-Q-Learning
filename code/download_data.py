import yfinance as yf

print("Downloading stock data...")

data = yf.download("AAPL", start="2020-01-01", end="2024-01-01")

data.to_csv("data/AAPL.csv")

print("Data downloaded and saved successfully!")