import datetime
import requests
import json
import pandas as pd
import numpy as np

class AmeriTradeHistoryDataService:
      """
        Class(a Service) to download stocks' or EFTs' historical price data by using AmeriTrade API.
      """
      def __init__(self, apiKey):
        #set up api key  
        self.apiKey=apiKey

      def __ParseResponse(self,responseText):
          """
            To parse json API response to dataframe.
            
            Paramaters
            ------------
            responseText:str,json
                The json api response.

          """
          data = json.loads(responseText)
      
          if "candles" not in data:
              raise ValueError("Data does not exist!")
          
          #converting json string to dataframe
          dataHistory=data["candles"]
          df=pd.DataFrame(dataHistory)
          df['datetime'] = pd.to_datetime(df['datetime'], unit='ms')
          df.columns=['Open','High','Low','Close','Volume','Date']
          df=df.set_index('Date')

          return df

      def GetHistoricalData(self,symbol,frequencyType,frequency,periodType,period=None,startDate=None,endDate=None,needExtendedHoursData=False):
        """
        Download historical data for a symbol. 
        
        Paramaters
        ------------
        -symbol        : security symbol. Ex:AAPL,
        -frequencyType : the type of frequency(minute,daily,weekly,monthly) with which a new historical data is formed.
        -frequency     : the number of the frequencyType to be included in each historical data row.
        -period        : The number of periods to show.
        -periodType    : the type of period(day,month,year,ytd) to show.
        -endDate       : last date for historical data.
        -startDate     : first date for historical data.

        Hints
        ------------
        Valid frequency Types by periodType (defaults marked with an asterisk):
        day: minute*
        month: daily, weekly*
        year: daily, weekly, monthly*
        ytd: daily, weekly*
        """

        
        if all(v is None for v in [periodType,period,startDate,endDate]):
            raise ValueError("Period or time internal should be provided.")
        
        epoch = datetime.datetime.utcfromtimestamp(0)
        apiurl="https://api.tdameritrade.com/v1/marketdata/"+symbol+"/pricehistory"
        url=apiurl+"?apikey="+self.apiKey+"&frequencyType="+frequencyType+"&frequency="+str(frequency)+"&needExtendedHoursData="+str(needExtendedHoursData)
        
        # if start date and end date exit, period is unnecessary
        if (startDate is not None) & (endDate is not None):
            #date should be converted to milliseconds since epoch for using API
            _startDate=int((startDate-epoch).total_seconds() * 1000.0)
            _endDate=int((endDate-epoch).total_seconds()*1000.0)
            url+="&startDate="+str(_startDate)+"&endDate="+str(_endDate)
        else:
            #if period exist, start date and end date will not be considered
            url+="&period="+str(period)
        #period type is necessart in url
        url+="&periodType="+periodType

        #calling the API
        response = requests.request("GET", url)
        #Parsing returned response text
        result=self.__ParseResponse(response.text)
        return result
