import backtrader as bt
import backtrader.indicators as btind
from Indicator.SuperTrendIndicator import SuperTrend 
from Strategies import BaseStrategy as bs

class SuperTrendStrategy(bs.BaseStrategy):
    params = (
        ('period', 10),
        ('multiplier', 3),
        ('apply_hurst_exponent',False),
        ('hurst_exponent_lag',20)
    )

    def __init__(self):
        # To control operation entries
        self.orderid = None
        self.hr = btind.HurstExponent(period=self.p.hurst_exponent_lag)
        self.st = SuperTrend(period = self.p.period, multiplier = self.p.multiplier)
        super().__init__()
   
    def next(self):
        if self.orderid:
           return

        #Check if stop loss is/will be applied
        if self.stop_loss():
            return;
        
        buy_condition=self.st < self.data
        sell_condition =self.data < self.st
        if self.p.apply_hurst_exponent:
            if self.hr<0.5:
                buy_condition=False
                sell_condition=False
       
        if self.position.size:
             if sell_condition:
                self.sell(size=self.position.size)
      
        elif buy_condition:
            size = int(self.broker.get_cash() / self.data)
            self.buy(size=size)