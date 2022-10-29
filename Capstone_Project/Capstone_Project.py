from ast import Lambda
import pandas as pd
from pickle import FALSE
import backtrader as bt
import pandas as pd
from Data.AmeriTradeHistoryDataService import AmeriTradeHistoryDataService
from NoiseReduction.KalmanFiltering import KalmanFiltering as kf
from Strategies import SuperTrendStrategy as sts
import backtrader.analyzers as btanalyzers
import datetime
import sys
from itertools import combinations

#ameritrade api key
ameriTradeApiKey="7BNQRFGNAKJL5XFOAGZE2LIUSWFJGE5G"

def run_backtest(securityCode,data,filtered_data,combination):
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
     apply_hurst_exponent=True if 'HE' in combination else False
     apply_stop_loss=True if 'Stop Loss' in combination else False
     apply_volatility_adjusted=True if 'Volatility Adjusted Stop Loss' in combination else False
     apply_noise_reduction=True if 'Noise Reduction' in combination else False
     print("============================================================================")
     print(f'Hurst Exponent: {apply_hurst_exponent}')
     print(f'Stop Loss:      {apply_stop_loss}')
     print(f'Noise Reduction:{apply_noise_reduction}')
     print(f'VA Stop Loss:   {apply_volatility_adjusted}')

     if apply_volatility_adjusted:
        cerebro.addstrategy(sts.SuperTrendStrategy,printout=True,apply_hurst_exponent=apply_hurst_exponent,apply_noise_reduction=apply_noise_reduction,apply_stop_loss=True,stop_loss_type='volatility_adjusted',stop_loss_percentage=0.04)
     elif apply_stop_loss:
        cerebro.addstrategy(sts.SuperTrendStrategy,printout=True,apply_hurst_exponent=apply_hurst_exponent,apply_noise_reduction=apply_noise_reduction,apply_stop_loss=True,stop_loss_type='static_percentage',stop_loss_percentage=0.04)
     else:
        cerebro.addstrategy(sts.SuperTrendStrategy,printout=True,apply_hurst_exponent=apply_hurst_exponent,apply_noise_reduction=apply_noise_reduction)
   
        

     #Add analyzers to analyze backtest results
     cerebro.addanalyzer(btanalyzers.SharpeRatio, _name='sharpe')
     cerebro.addanalyzer(bt.analyzers.TradeAnalyzer, _name="ta")
     cerebro.addanalyzer(bt.analyzers.DrawDown, _name="dd")
     cerebro.addanalyzer(bt.analyzers.TimeDrawDown, _name="tdd")

     #set initial cask
     cerebro.broker.setcash(100000)
     cerebro.broker.setcommission(commission=0.001,commtype="COMM_FIXED")

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
     
     print("============================================================================")
     #Plotting
     cerebro.plot()
     return [apply_hurst_exponent,apply_noise_reduction,apply_stop_loss,apply_volatility_adjusted, numberOfTrade,profit_rate,strike_rate,pnl_net,max_drawdown,sharpe_ratio]

def apply_backtest_for_security(securityCode,startDate,endDate,frequency,combination):
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
    #try:
        #Download historical data
    if frequency == "Daily":
        HistoricalDataService = AmeriTradeHistoryDataService(ameriTradeApiKey) 
        data = HistoricalDataService.GetHistoricalData(securityCode,"daily",1,startDate=startDate,endDate=endDate,periodType="year")
    elif frequency == "Hourly":
        HistoricalDataService = AmeriTradeHistoryDataService(ameriTradeApiKey)
        data = HistoricalDataService.GetHistoricalData(securityCode,"minute",60,startDate=startDate,endDate=endDate,periodType="day")
    #except:
    #     print("Historical data can not be downloaded!")
    #     return
    filtered_data = kf(data)
    #Run backtest
    return run_backtest(securityCode,data,filtered_data,combination)


if __name__ == "__main__":
     #all conditions
     conditions=['HE','Stop Loss','Noise Reduction','Volatility Adjusted Stop Loss']

     #all combination of conditions
     condition_combinations=list()
     for n in range(len(conditions)+1):
         combination=list(combinations(conditions,n))
         condition_combinations+= combination
     #make sure Stop loss and Volatility Adjusted Stop Loss will not applied same time
     condition_combinations=list(filter(lambda c:not ('Stop Loss' in c and 'Volatility Adjusted Stop Loss' in c),condition_combinations))
     condition_combinations=[[]]
     #print(condition_combinations)
    
     #Get all securities(ETFs)
     securities=['SPY','QQQ']
     #Get all strategies
     '''strategies=[
         {
            'TimeFrame':'Since 2019-1-1',
            'StartDate':datetime.datetime(2019,1, 1),
            'EndDate':datetime.datetime(2022,10, 10),
            'Frequency':'Hourly',
            'Apply'

         },
         {
             #Strategy 3
            'StrategyName':'Supertrend',
            'StrategyId':'Supertrend',
            'TimeFrame':'During Pandemic(01 Jan 2019 - 13 Jul 2022)',
            'StartDate':datetime.datetime(2019,1, 1),
            'EndDate':datetime.datetime(2022,10, 13),
            'Frequency':'Daily'
         },
         {
             #Strategy 4
            'StrategyName':'Supertrend+HE+Noise Reduction+Volatility Adjusted Stop Loss',
            'StrategyId':'Supertrend+HE+Noise Reduction+Volatility Adjusted Stop Loss',
            'TimeFrame':'During Pandemic(01 Jan 2019 - 13 Jul 2022)',
            'StartDate':datetime.datetime(2019,1, 1),
            'EndDate':datetime.datetime(2022,10, 13),
            'Frequency':'Daily'
         }
     ]'''
     dateStartDate=datetime.datetime(2019,1, 1)
     dateEndDate=datetime.datetime(2022,10, 10)
     frequency='Hourly'
     all_results=[]
     #iterate all securities
     for security in securities:
        securityCode=security
        print(f'**************{securityCode}****************')
        print(f'Start Date:     {dateStartDate}')
        print(f'End Date:       {dateEndDate}')
        print(f'Frequency:      {frequency}')
        #iterate all combinations
        for combination in condition_combinations:
            #apply backtest for a current security and strategy
            result=apply_backtest_for_security(securityCode,dateStartDate,dateEndDate,frequency,combination)
            all_results.append(result)
     df = pd.DataFrame(all_results, columns =['HE','Noise Reduction','Stop Loss','VA Stop Loss', '# of Trade','Profit Rate','Strike Rate','PnL','Max Drawdown','Sharpe Ratio'], dtype = float)
     df.to_csv(f"{frequency}.csv",index="Date")  
    
 