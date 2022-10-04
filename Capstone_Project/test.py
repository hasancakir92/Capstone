from pickle import FALSE
import backtrader as bt

from Data.AmeriTradeHistoryDataService import AmeriTradeHistoryDataService
from Strategies import RSIStrategy as rsi
from Data import BacktestResultDB as db
import backtrader.analyzers as btanalyzers
import backtrader as bt
import backtrader.indicators as btind
from Indicator.SuperTrendIndicator import SuperTrend 
import datetime

class SuperTrendStrategy(bt.Strategy):


    def __init__(self):
        # To control operation entries
        self.orderid = None
        self.st = SuperTrend(period = 10, multiplier = 3)
        super().__init__()
   
    def next(self):
        if self.orderid:
           return
    
        if self.position.size:
             if self.data < self.st:
                self.sell(size=self.position.size)

        elif self.st < self.data:
            size = int(self.broker.get_cash() / self.data)
            self.buy(size=size)
       
cerebro = bt.Cerebro()
     
cerebro.addstrategy(SuperTrendStrategy)
     
  
cerebro.broker.setcash(10000)
HistoricalDataService = AmeriTradeHistoryDataService("7BNQRFGNAKJL5XFOAGZE2LIUSWFJGE5G")
startDate=datetime.datetime(2019,1, 1)
endDate=datetime.datetime(2022,8, 26)
data = HistoricalDataService.GetHistoricalData("AAPL","daily",1,startDate=startDate,endDate=endDate,periodType="year")

#Feed strategy with data
backtestData= bt.feeds.PandasData(dataname=data)
cerebro.adddata(backtestData)

#Running Backtest
thestrats=cerebro.run()
cerebro.plot()
     