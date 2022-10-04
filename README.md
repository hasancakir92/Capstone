# MSCFE 690 - Capstone Project - Risk Management in Short Term Mean-Reverting Trading

In a mean reverting strategy, it is assumed that prices of a security will revert 
towards to mean after a big drop or big increase on prices of the security. The main problem 
on this assumption is that price return of a security mostly is not stationary and not normally 
distributed, so it will hard to find out when the price of an asset will return to the mean. 
Moreover, those unexpected moves in price can also lead to a shift in its normal or mean.

Therefore, in this project I will try creating a concept about what kind of risk 
mitigation techniques can be used to avoid big losses while applying mean-reverting trading 
strategies. I will implement mean-reverting strategies with risk management techniques, 
then I will backtest those strategies with ETFs historical data.

Each ETF was backtested by using RSI signals according to below criteria:
- without any risk management technique
- with static percentage stop loss
- with volatility adjusted percentage stop loss
- with time based stop
- with volatility adjusted position resizing 

### 1. Solution
![General Architecture of Project](https://github.com/hasancakir92/Capstone_Project/blob/master/General%20Architecture.jpg)
### 2. Code Structure

    .
    ├── Data                                         # Folder - Services related with data transactions
    │   ├── AmeriTradeHistoryDataService.py          # Download historical price data for a security by using AmeriTrade API
    │   ├── BacktestResultDB.py                      # Manage database transaction to save backtest result for further analysis
    ├── Strategies                                   # Folder - Strategies for backtesting
    │   ├── BaseStrategy.py                          # Generic abstract base class that can be interface for different strategies.
    │   ├── RSIStrategy.py                           # Implementation of RSI strategy derived from BaseStrategy
    ├── Capstone_Project.py                          # Implementation of backtesting process
    └── README.md
#### Data Folder
An abstract class (AmeriTradeHistoryDataService.py) was implemented to download historical data by using AmeriTrade historical data api([Documentation](https://developer.tdameritrade.com/content/price-history-samples),[Usage](https://developer.tdameritrade.com/price-history/apis/get/marketdata/%7Bsymbol%7D/pricehistory)). 

AmeriTrade api key should be entered in Capstone_Project.py file. You need to register an app after creating a developer account in AmeriTrade. After, an app registered, system will give you an API key ([Openning Developer Account and Registering an APP](https://developer.tdameritrade.com/content/getting-started)).
```
#ameritrade api key
ameriTradeApiKey=""
```
In order to save backtest result for each ETF and strategy, a method under BacktestResultDB.py was develop. Moreover, two more functions was developed to read all ETFs and strategies that will be backtested from database. MSSQL SQL Express([Download](https://www.microsoft.com/en-US/sql-server/sql-server-downloads), [Installation](https://www.sqlshack.com/how-to-install-sql-server-express-edition/)) is used as database in this project. Then, connection string should be changed in BacktestResultDB.py file.

```
#connection string to connect db
conn = pyodbc.connect('')
```

#### Strategies Folder
Firstly, a base strategy class(BaseStrategy.py) was implemented to give generic approach for any strategy. Any strategy derived from this class will have below methods:
 - To notify about order situation
 - To printout any log
 - To notify about trade situation when a trade is closed or open.
 - To apply stop loss(static percentage or volatility adjusted) for any strategy
 - To apply time based stop loss
 - To apply position sizing based on volatility
 
 Secondly, a strategy class(RSIStrategy.py) was derived from BaseStrategy. It includes buy and signal logic based on RSI indicator.
 
    ### For more details, comments in source code can be checked. ###
### 3. Database
In database, we have three tables:
1. Security: it keeps the all ETFs' symbol and description. Any securities inside this table will be backtested.
2. Strategy : it keeps strategies that will be backtested and their setup information like time frequency, start and end date of historical data.
3. StrategyResult: it keeps all backtest result like profit rate, PnL, Max Drawdown, Sharpe Ratio and Number of Trade processed for each ETF and strategy. 

[CapstoneProject.sql](https://github.com/hasancakir92/Capstone_Project/blob/master/CapstoneProject.sql) file includes all table schemas about the database. Moreover, insertion script for ETFs and strategies can be found inside it.
