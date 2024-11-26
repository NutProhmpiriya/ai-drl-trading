import MetaTrader5 as mt5

if not mt5.initialize():
    print("no connection to MetaTrader 5")
    mt5.shutdown()
else: 
    print("connection to MetaTrader 5 established")
    mt5.shutdown()