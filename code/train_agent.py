from environment.trading_env import TradingEnvironment
from agent.q_learning_agent import QLearningAgent

env = TradingEnvironment("data/AAPL.csv")
agent = QLearningAgent(actions=[0, 1, 2])  # Hold, Buy, Sell

episodes = 10

for episode in range(episodes):
    state = env.reset()
    total_reward = 0

    while True:
        action = agent.choose_action(state)
        next_state, reward, done = env.step(action)
        agent.learn(state, action, reward, next_state)

        state = next_state
        total_reward += reward

        if done:
            print(f"Episode {episode+1} | Total Profit: {round(total_reward,2)}")
            break