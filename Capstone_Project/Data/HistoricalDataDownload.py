from Data.AmeriTradeHistoryDataService import AmeriTradeHistoryDataService
import datetime
import pandas as pd

ameriTradeApiKey="7BNQRFGNAKJL5XFOAGZE2LIUSWFJGE5G"
HistoricalDataService = AmeriTradeHistoryDataService(ameriTradeApiKey) 

def DowloadHistoricalData(startDate, endDate,securityCode,minute):
    '''
    We will dowload minute data with 2 days bundle 
    '''
    _dataDownloadStartDate=startDate
    _dataDownloadEndDate=startDate
    finaldata=pd.DataFrame()
    #While bundle end date does not reach requested end date 
    while _dataDownloadEndDate+datetime.timedelta(days=2)<endDate:
        _dataDownloadEndDate=_dataDownloadStartDate+datetime.timedelta(days=2)
        
        #download data for two days
        print(f"Downloading data for {securityCode} between {_dataDownloadStartDate} and {_dataDownloadEndDate}")
        try:
            data = HistoricalDataService.GetHistoricalData(securityCode,"minute",minute,startDate=_dataDownloadStartDate,endDate=_dataDownloadEndDate,periodType="day")
            finaldata = pd.concat([finaldata,data])
        except:
            print("Historical data can not be downloaded!")
        _dataDownloadStartDate=_dataDownloadEndDate+datetime.timedelta(days=1)
    
        # if there are remaining days from bundle
    if _dataDownloadStartDate<=endDate:
        _dataDownloadStartDate=_dataDownloadEndDate+datetime.timedelta(days=1)
        _dataDownloadEndDate=endDate
        print(f"Downloading data for {securityCode} between {_dataDownloadStartDate} and {_dataDownloadEndDate}")
        try:
            data = HistoricalDataService.GetHistoricalData(securityCode,"minute",minute,startDate=_dataDownloadStartDate,endDate=_dataDownloadEndDate,periodType="day")
            finaldata = pd.concat([finaldata,data])
        except:
            print("Historical data can not be downloaded!")
    # save as csv
    finaldata.to_csv(f"{securityCode}.csv",index="Date")  
    #return finaldata
#1 minute data can be just downloaded starting from 2022-9-1
#3 minute data can not be downloaded
#5 minute data can be just downloaded starting from 2022-2-1
#60 minute data can be just downloaded starting from 2021-6-1

securityCode="QQQ"
startDate=datetime.datetime(2021,5,1,4,0,0)
endDate=datetime.datetime(2022,10,13,4,0,0)
DowloadHistoricalData(startDate,endDate,securityCode,60)

   