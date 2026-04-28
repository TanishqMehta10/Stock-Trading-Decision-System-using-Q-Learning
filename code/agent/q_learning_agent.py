import random
import numpy as np

class QLearningAgent:
    def __init__(self, actions):
        self.q_table = {}              # Q[state] = [Q_hold, Q_buy, Q_sell]
        self.actions = actions
        self.alpha = 0.1               # learning rate
        self.gamma = 0.95              # future reward importance
        self.epsilon = 1.0             # exploration rate
        self.epsilon_decay = 0.995
        self.epsilon_min = 0.01

    def get_state_key(self, state):
        # Convert float values to rounded values for table indexing
        price, stock, balance = state
        return (round(price, 2), stock, round(balance, 2))

    def choose_action(self, state):
        state_key = self.get_state_key(state)

        if state_key not in self.q_table:
            self.q_table[state_key] = [0, 0, 0]

        # Exploration vs Exploitation
        if random.random() < self.epsilon:
            return random.choice(self.actions)
        else:
            return np.argmax(self.q_table[state_key])

    def learn(self, state, action, reward, next_state):
        state_key = self.get_state_key(state)
        next_key = self.get_state_key(next_state)

        if next_key not in self.q_table:
            self.q_table[next_key] = [0, 0, 0]

        old_value = self.q_table[state_key][action]
        next_max = max(self.q_table[next_key])

        # Q-Learning formula
        new_value = old_value + self.alpha * (
            reward + self.gamma * next_max - old_value
        )

        self.q_table[state_key][action] = new_value

        # Reduce exploration slowly
        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay