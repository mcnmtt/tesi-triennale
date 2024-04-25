import talib
from backtesting import Backtest, Strategy
from backtesting.test import GOOG
from backtesting.lib import crossover

def run_backtest(upper_bound, lower_bound, rsi_window):

    class RsiOscillator(Strategy):

        def init(self):
            self.rsi = self.I(talib.RSI, self.data.Close, rsi_window)

        def next(self):

            price = self.data.Close[-1]
        
            if crossover(self.rsi, upper_bound): 
                self.position.close()
                self.sell(sl=price*1.15, tp=0.95*price)
            elif crossover(lower_bound, self.rsi):
                self.buy(tp=price*1.15, sl=0.95*price)
                self.position.close()

    bt = Backtest(GOOG, RsiOscillator, cash=10000, commission=0.002)
    stats = bt.run()

    # Prendo i dati utili per la fitness normalizzandoli. Saranno valori compresi tra 0 e 1.

    max_drawdown = stats['Max. Drawdown [%]']/100
    return_value = stats['Return [%]']/100
    win_rate = stats['Win Rate [%]']/100
    num_trade = stats['# Trades']/100

    return_stats = [max_drawdown, return_value, win_rate, num_trade]
    
    return return_stats
