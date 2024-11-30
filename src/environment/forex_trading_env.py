import gymnasium as gym
import numpy as np 
import MetaTrader5 as mt5

class ForexTradingEnv(gym.Env):
    def __init__(self):
        super(ForexTradingEnv, self).__init__()
        
        pass

    def rest(self):
        return self._get_state()

    def _get_state(self):
        
        pass

    def step(self, action):
        pass

    def render(self):
        pass

