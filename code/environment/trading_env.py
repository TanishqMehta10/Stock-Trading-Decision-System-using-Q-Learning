import pandas as pd

class TradingEnvironment:
    def __init__(self, csv_path):
        # Load CSV
        self.data = pd.read_csv(csv_path)

        # Ensure Close price is numeric
        self.data["Close"] = pd.to_numeric(self.data["Close"], errors="coerce")

        # Remove NaN rows and reset index
        self.data = self.data.dropna().reset_index(drop=True)

        # Environment variables
        self.current_step = 0
        self.balance = 10000      # starting money
        self.stock_owned = 0
        self.done = False

    def reset(self):
        self.current_step = 0
        self.balance = 10000
        self.stock_owned = 0
        self.done = False
        return self._get_state()

    def _get_state(self):
        price = float(self.data.loc[self.current_step, "Close"])
        return [price, self.stock_owned, self.balance]

    def step(self, action):
        """
        Actions:
        0 = Hold
        1 = Buy
        2 = Sell
        """

        price = float(self.data.loc[self.current_step, "Close"])
        reward = 0

        # BUY
        if action == 1:
            if self.balance >= price:
                self.stock_owned += 1
                self.balance -= price

        # SELL
        elif action == 2:
            if self.stock_owned > 0:
                self.stock_owned -= 1
                self.balance += price
                reward = price   # profit as reward

        # Move to next day
        self.current_step += 1

        # End of data
        if self.current_step >= len(self.data) - 1:
            self.done = True

        next_state = self._get_state()
        return next_state, reward, self.done