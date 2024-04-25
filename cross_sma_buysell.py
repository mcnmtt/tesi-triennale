from backtesting import Backtest, Strategy
from backtesting.lib import crossover

from backtesting.test import SMA, GOOG

def run_backtest(sma1, sma2):

    class SmaCross(Strategy):

        def init(self):

            close = self.data.Close
            self.sma1 = self.I(SMA, close, sma1)
            self.sma2 = self.I(SMA, close, sma2)

        def next(self):

            price = self.data.Close

            if crossover(self.sma1, self.sma2):
                self.buy(sl=price*0.90)
            elif crossover(self.sma2, self.sma1):
                self.sell(sl=price*1.10)

    bt = Backtest(GOOG, SmaCross, cash=10000, commission=0.002)
    stats = bt.run()

    # Prendo i dati utili per la fitness normalizzandoli. Saranno valori compresi tra 0 e 1.

    return_value = stats['Equity Final [$]']/100

    return return_value

