from environment.trading_env import TradingEnvironment

# Create environment
env = TradingEnvironment("data/AAPL.csv")

# Reset environment
state = env.reset()
print("Initial State:", state)

# Test with fixed BUY actions
for step in range(5):
    action = 1  # BUY
    next_state, reward, done = env.step(action)
    print(f"Step {step+1} | State: {next_state} | Reward: {reward}")