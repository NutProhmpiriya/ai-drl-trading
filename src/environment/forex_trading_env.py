import gymnasium as gym
import numpy as np 
import MetaTrader5 as mt5

class ForexTradingEnv(gym.Env):
    def __init__(self, symbol="EURUSD")
        super(ForexTradingEnv, self).__init__()
        self.symbol = symbol
        self.action_space = gym.spaces.Discrete(3) # 0 = buy, 1 = sell, 2 = hold 
        self.observation_space = gym.spaces.Box(
            low=0, 
            high=np.inf, 
            shape=(5,), 
            dtype=np.float32
        )  # Example state: price, technical indicators

    def rest(self):
        self.balnce = 10000
        self.position = 0 
        self.price_history = [] # store price history
        self.current_step = 0
        return self._get_state()

    def _get_state(self):
        # example state could be a combination of price and technical indicators
        price = mt5.symbol_info_tick(self.symbol).ask
        return np.array([price, 0 ,0 ,0 ,0]) # example state with dummy indicators

    def step(self, action):
        state = self._get_state()
        done = False

        if action == 0: # buy
            self.position = 1
        elif action == 1: # sell
            self.position = -1
        elif action == 2: # hold
            pass 

        # calculate reward
        reward = 0  # you can calculate this base on the profit/loss from position
        self.price_history.append(state[0]) # recode the price for historical tracking
        return state, reward, done, {}

    def render(self):
        # render the environment
        pass
    
