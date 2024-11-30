import gymnasium as gym
import numpy as np
import pandas as pd
import plotly.graph_objects as go

class ForexEnv(gym.Env):
    def __init__(self, data, initial_balance=10000, max_daily_loss=0.01, window_size=50, risk_per_trade=0.01, leverage=50):
        super(ForexEnv, self).__init__()

        self.data = data
        self.initial_balance = initial_balance
        self.max_daily_loss = max_daily_loss
        self.window_size = window_size
        self.risk_per_trade = risk_per_trade
        self.leverage = leverage

        self.current_step = self.window_size
        self.balance = self.initial_balance
        self.position = 0
        self.entry_price = 0
        self.stop_loss = 0
        self.take_profit = 0
        self.daily_loss = 0

        self.action_space = gym.spaces.Discrete(3)  # 0 = Buy, 1 = Hold, 2 = Sell
        self.observation_space = gym.spaces.Box(low=-np.inf, high=np.inf, shape=(self.window_size, 4), dtype=np.float32)

        self.balance_history = [self.balance]
        self.max_drawdown = 0
        self.trades = 0
        self.win_trades = 0

    def reset(self):
        self.current_step = self.window_size
        self.balance = self.initial_balance
        self.position = 0
        self.entry_price = 0
        self.stop_loss = 0
        self.take_profit = 0
        self.daily_loss = 0
        self.balance_history = [self.balance]
        self.max_drawdown = 0
        self.trades = 0
        self.win_trades = 0
        return self.get_observation(), {}

    def get_observation(self):
        obs = self.data.iloc[self.current_step - self.window_size:self.current_step][['Open', 'High', 'Low', 'Close']].values
        return np.array(obs)

    def calculate_atr(self):
        atr_period = 14
        high = self.data['High']
        low = self.data['Low']
        close = self.data['Close'].shift(1)
        tr = pd.concat([high - low, abs(high - close), abs(low - close)], axis=1).max(axis=1)
        return tr.rolling(window=atr_period).mean().iloc[self.current_step]

    def step(self, action):
        high_price = self.data.iloc[self.current_step]['High']
        low_price = self.data.iloc[self.current_step]['Low']
        close_price = self.data.iloc[self.current_step]['Close']
        spread = self.data.iloc[self.current_step]['Spread']

        bid_price = low_price - spread / 2
        ask_price = high_price + spread / 2
        reward = 0
        done = False

        atr = self.calculate_atr()

        if action == 0 and self.position == 0:  # Buy
            position_size = self.calculate_position_size(ask_price)
            self.position = 1
            self.entry_price = ask_price
            self.stop_loss = ask_price - atr
            self.take_profit = ask_price + 2 * atr
            self.balance -= position_size * ask_price
        elif action == 2 and self.position == 0:  # Sell
            position_size = self.calculate_position_size(bid_price)
            self.position = -1
            self.entry_price = bid_price
            self.stop_loss = bid_price + atr
            self.take_profit = bid_price - 2 * atr
            self.balance += position_size * bid_price

        if self.position == 1:
            if bid_price <= self.stop_loss or bid_price >= self.take_profit:
                self.trades += 1
                if bid_price >= self.take_profit:
                    self.win_trades += 1
                reward = (bid_price - self.entry_price) * position_size
                self.balance += position_size * bid_price
                self.position = 0
        elif self.position == -1:
            if ask_price >= self.stop_loss or ask_price <= self.take_profit:
                self.trades += 1
                if ask_price <= self.take_profit:
                    self.win_trades += 1
                reward = (self.entry_price - ask_price) * position_size
                self.balance -= position_size * ask_price
                self.position = 0

        self.balance_history.append(self.balance)
        self.max_drawdown = min(self.max_drawdown, (min(self.balance_history) - self.initial_balance) / self.initial_balance)

        self.current_step += 1
        if self.current_step >= len(self.data) - 1 or self.balance < self.initial_balance * (1 - self.max_daily_loss):
            done = True

        return self.get_observation(), reward, done, {}

    def calculate_position_size(self, current_price):
        stop_loss_distance = abs(current_price - self.stop_loss)
        position_size = (self.balance * self.risk_per_trade) / stop_loss_distance
        return position_size * self.leverage

    def render(self):
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=list(range(len(self.balance_history))), y=self.balance_history, mode='lines', name='Balance'))
        fig.update_layout(
            title="Balance Over Time",
            xaxis_title="Steps",
            yaxis_title="Balance",
            showlegend=True
        )
        fig.show()
