"""
Created on Sat Oct  8 16:10:09 2022

@author: Admin
"""

from pykalman import KalmanFilter
import pandas as pd



# Construct a Kalman filter:
    #The mean is the model's guess for the mean of the distribution from which 
    #measurements are drawn, so our prediction of the next value is simply equal to our estimate of the mean. 
    #We assume that the observations have variance 1 around the rolling mean, for lack of a better estimate. Our initial guess for the mean is 0, 
    #but the filter quickly realizes that that is incorrect and adjusts.

def KalmanFiltering(data):
    
    data_series = data['Close'].squeeze()
    
    kf = KalmanFilter(transition_matrices = [1],
                  observation_matrices = [1],
                  initial_state_mean = 0,
                  initial_state_covariance = 1,
                  observation_covariance=1,
                  transition_covariance=.01)
    
    state_means, _ = kf.filter(data_series.values)
    state_means = pd.Series(state_means.flatten(), index=data.index)
    
    df_Kalman = data[['Open', 'High', 'Low', 'Volume']]
    df_Kalman['Close'] = state_means
    
    return df_Kalman


#The advantage of the Kalman filter is that we don't need to select a window length, so we run less risk of overfitting. 
#We do open ourselves up to overfitting with some of the initialization parameters for the filter, but those are slightly easier to objectively define. 
#There's no free lunch and we can't eliminate overfitting, but a Kalman Filter is more rigorous than a moving average and generally better.

