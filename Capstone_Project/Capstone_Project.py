from pickle import FALSE
import backtrader as bt

from Data.AmeriTradeHistoryDataService import AmeriTradeHistoryDataService
from NoiseReduction.KalmanFiltering import KalmanFiltering as kf
from Strategies import SuperTrendStrategy as sts
import backtrader.analyzers as btanalyzers
import datetime
import sys


#ameritrade api key
ameriTradeApiKey="7BNQRFGNAKJL5XFOAGZE2LIUSWFJGE5G"

def run_backtest(securityCode,data,filtered_data,strategyId,strategyName):
     """
        Runs backtrader engine to process backtest

        Paramaters:
        -------------
        securityCode:str
            security that will be backtest Ex. AAPL, MSFT etc.
        data:dataframe
            historical price data for security
        strategyId:str
            id of strategy that will be applied, we will save result to db with this id
        strategyName:
            name of the strategy
            
     """

     #Backtesting engine
     cerebro = bt.Cerebro()
     
     # Without Risk Management
     if strategyName=="Supertrend":
        cerebro.addstrategy(sts.SuperTrendStrategy,printout=True,apply_noise_reduction=True)
        
     # With HE
     if strategyName=="Supertrend+HE":
        cerebro.addstrategy(sts.SuperTrendStrategy,printout=True,apply_hurst_exponent=True)
     

     # with Static Percentage Stop Loss
     if strategyName=="Supertrend+Stop Loss":
        cerebro.addstrategy(sts.SuperTrendStrategy,printout=True,apply_stop_loss=True,stop_loss_type='static_percentage',stop_loss_percentage=0.02)

     # with Volatility Adjusted Stop Loss
     if strategyName=="Supertrend+Volatility Adjusted Stop Loss":
        cerebro.addstrategy(sts.SuperTrendStrategy,printout=True,apply_stop_loss=True,stop_loss_type='volatility_adjusted',stop_loss_percentage=0.02)

 

     #Add analyzers to analyze backtest results
     cerebro.addanalyzer(btanalyzers.SharpeRatio, _name='sharpe')
     cerebro.addanalyzer(bt.analyzers.TradeAnalyzer, _name="ta")
     cerebro.addanalyzer(bt.analyzers.DrawDown, _name="dd")
     cerebro.addanalyzer(bt.analyzers.TimeDrawDown, _name="tdd")

     #set initial cask
     cerebro.broker.setcash(100000)
    
     #Feed strategy with data
     backtestData= bt.feeds.PandasData(dataname=data)
     cerebro.adddata(backtestData)

     #Feed strategy with filtered data
     filteredData= bt.feeds.PandasData(dataname=filtered_data)
     cerebro.adddata(filteredData)

     #Get initial portfolip value
     initial_portfolio_value=cerebro.broker.getvalue();

     #Running Backtest
     thestrats=cerebro.run()
     thestrat = thestrats[0]

     #Get Final Portfolio Value
     final_portfolio_value = cerebro.broker.getvalue()

     #calculate profit rate
     profit_rate=(final_portfolio_value-initial_portfolio_value)/initial_portfolio_value

     #get trade analysis
     result=thestrat.analyzers.ta.get_analysis()
 
     strike_rate=None
     pnl_net=None
     max_drawdown=None
     sharpe_ratio=None
     numberOfTrade=result.total.total

     print("# of Trade        :%.3f" % numberOfTrade)
     print("Profit Rate       :%.3f" % profit_rate)
     if numberOfTrade>0:
        total_closed = result.total.closed
        total_won = result.won.total

        #calculate strike rate(success rate) for traders
        strike_rate = (total_won / total_closed) * 100
        print("Strike Rate       :%.3f" % strike_rate)

        #get PnL results
        pnl_net = round(result.pnl.net.total,2)
        print("PnL net           :%.3f" % pnl_net)

        #get max drawdown
        max_drawdown=thestrat.analyzers.dd.get_analysis().max.drawdown
        print("Max DrawDown      :%.3f percent" % max_drawdown)
        
        #get Sharpe Ratio
        sharpe_ratio=thestrat.analyzers.sharpe.get_analysis()['sharperatio']
        print("Sharpe Ratio      :%.3f" % sharpe_ratio) 
     
    
     #Plotting
     cerebro.plot()

def apply_backtest_for_security(securityCode,strategyId,strategyName,startDate,endDate):
    """
        To apply backtess for a security
        Paramaters:
        -------------
        securityCode:str
            security that will be backtest Ex. AAPL, MSFT etc.
        strategyId:str
            id of strategy that will be applied, we will save result to db with this id
        strategyName:str
            name of the strategy
        startDate:datetime
            start date of historical data need to be downloaded
        endDate:datetime
            end date of historical data need to be downloaded
    """
    try:
        #Download historical data
        HistoricalDataService = AmeriTradeHistoryDataService(ameriTradeApiKey) 
        data = HistoricalDataService.GetHistoricalData(securityCode,"daily",1,startDate=startDate,endDate=endDate,periodType="year")
    except:
         print("Historical data can not be downloaded!")
         return
    filtered_data = kf(data)
    #Run backtest
    run_backtest(securityCode,data,filtered_data,strategyId,strategyName)


if __name__ == "__main__":
     #Get all securities(ETFs)
     securities=['QQQ']
     #Get all strategies
     strategies=[
         {
            'StrategyName':'Supertrend',
            'StrategyId':'Supertrend',
            'TimeFrame':'During Pandemic(01 Jan 2019 - 13 Jul 2022)',
            'StartDate':datetime.datetime(2019,1, 1),
            'EndDate':datetime.datetime(2022,10, 2)
         },
         {
            'StrategyName':'Supertrend+Stop Loss',
            'StrategyId':'Supertrend+Stop Loss',
            'TimeFrame':'During Pandemic(01 Jan 2019 - 13 Jul 2022)',
            'StartDate':datetime.datetime(2019,1, 1),
            'EndDate':datetime.datetime(2022,10, 2)
         },
         {
            'StrategyName':'Supertrend+Volatility Adjusted Stop Loss',
            'StrategyId':'Supertrend+Volatility Adjusted Stop Loss',
            'TimeFrame':'During Pandemic(01 Jan 2019 - 13 Jul 2022)',
            'StartDate':datetime.datetime(2019,1, 1),
            'EndDate':datetime.datetime(2022,10, 2)
         },
          {
            'StrategyName':'Supertrend+HE',
            'StrategyId':'Supertrend+HE',
            'TimeFrame':'During Pandemic(01 Jan 2019 - 13 Jul 2022)',
            'StartDate':datetime.datetime(2019,1, 1),
            'EndDate':datetime.datetime(2022,10, 2)
         }
         
     ]
     
     #iterate all securities
     for security in securities:
        securityCode=security
        print(f'==>{securityCode}')
        #iterate all strategies
        for strategy in strategies:
            strategyName=strategy["StrategyName"]
            strategyId=strategy["StrategyId"]
            timeFrame=strategy["TimeFrame"]
            dateStartDate=strategy["StartDate"]
            dateEndDate=strategy["EndDate"]
            print(f'====>{strategyName} for {timeFrame} in on process!')
            #apply backtest for a current security and strategy
            apply_backtest_for_security(securityCode,strategyId,strategyName,dateStartDate,dateEndDate)
  