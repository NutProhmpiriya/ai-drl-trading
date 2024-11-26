import MetaTrader5 as mt5 
import pandas as pd 

class MT5Env: 
    def __init__(self, symbol="EURUSD", timeframe=mt5.TIMEFRAME_M1,):
        self.symbol = symbol 
        self.timeframe = timeframe
        self.initialize_mt5()

    