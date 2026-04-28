import pandas as pd
import matplotlib.pyplot as plt

# Properly load CSV (skip extra header row)
data = pd.read_csv("data/AAPL.csv", skiprows=2)

# Rename columns properly
data.columns = ["Date", "Close", "High", "Low", "Open", "Volume"]

# Convert Close column to numeric
data["Close"] = pd.to_numeric(data["Close"], errors="coerce")

# Remove missing values
data = data.dropna()

print(data.head())

# Plot closing price
plt.figure(figsize=(10,5))
plt.plot(data["Close"])
plt.title("AAPL Stock Price")
plt.xlabel("Days")
plt.ylabel("Price")
plt.show()