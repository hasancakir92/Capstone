# MSCFE 690 - Capstone Project - Usage of the Hurst Exponent for Short Term Trading Strategies

The goal of this research paper is to build trend following strategies for intraday
trading by using the Hurst Exponent and combining it with technical indicators such as
the SuperTrend or MACD indicators. First, we attempt to minimize the white noise effect
of the Hurst Exponent. Going further, we will use the Hurst Exponent to identify trending
and mean-reverting time series, based on this we will use the signals of the SuperTrend
indicator to enter into position. We will use backtader.py for back testing on Index ETFs
such as SPY, QQQ and IWM, on 1, 3 and 5 minute timeframes.

### 1. Solution
![General Architecture of Project](https://github.com/hasancakir92/Capstone/blob/master/General%20Architecture.jpg)
### 2. Code Structure

    .
    ├── Data                                         # Folder - Services related with data transactions
    │   ├── AmeriTradeHistoryDataService.py          # Download historical price data for a security by using AmeriTrade API
    ├── Strategies                                   # Folder - Strategies for backtesting
    │   ├── BaseStrategy.py                          # Generic abstract base class that can be interface for different strategies.
    │   ├── SuperTrendStrategy.py                    # Implementation of Supertrend strategy derived from BaseStrategy
    ├── Capstone_Project.py                          # Implementation of backtesting process
    └── README.md
#### Data Folder
An abstract class (AmeriTradeHistoryDataService.py) was implemented to download historical data by using AmeriTrade historical data api([Documentation](https://developer.tdameritrade.com/content/price-history-samples),[Usage](https://developer.tdameritrade.com/price-history/apis/get/marketdata/%7Bsymbol%7D/pricehistory)). 

AmeriTrade api key should be entered in Capstone_Project.py file. You need to register an app after creating a developer account in AmeriTrade. After, an app registered, system will give you an API key ([Openning Developer Account and Registering an APP](https://developer.tdameritrade.com/content/getting-started)).
```
#ameritrade api key
ameriTradeApiKey=""
```
#### Strategies Folder
Firstly, a base strategy class(BaseStrategy.py) was implemented to give generic approach for any strategy. Any strategy derived from this class will have below methods:
 - To notify about order situation
 - To printout any log
 - To notify about trade situation when a trade is closed or open.
 - To apply stop loss(static percentage or volatility adjusted) for any strategy
 
 Secondly, a strategy class(SuperTrendStrategy.py) was derived from BaseStrategy. It includes buy and signal logic based on Supertrend indicator and Hurst Exponent.
 
