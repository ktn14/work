# -*- coding: utf-8 -*-
"""
Created on Tue Oct  2 17:19:37 2018

@author: ktn14
"""


#DES Method
import pandas as pd
df_grocery = pd.read_excel('grocery_data.xlsx')

# remove first row and first column 
import numpy as np
df_grocery = df_grocery.iloc[1:,:16]

# rename columns
df_grocery.columns = np.arange(1,17)
df_count = df_grocery.count(axis=1)

# remove last observation wth data for each day
for i in range(1,21):
    if df_grocery.isnull().any(axis = 1).loc[i]:
        df_grocery.loc[i,df_count[i]] = np.nan   
        
#cumulative sum df
df_cumsales = np.cumsum(df_grocery,axis=1)

# censored column
df_cumsales['censored'] = df_count !=16

# create df_des df using only censored rows
df_des = df_cumsales[df_cumsales.censored].drop('censored',axis=1)

from sklearn.metrics import mean_squared_error
from statsmodels.tsa.api import ExponentialSmoothing
from itertools import product
import itertools as it

# write a function that takes alpha,beta,series as input and produces the traning sample MSE, allow 3 periods for burn-in
def DESMSE(alpha,beta,series):
    return mean_squared_error(series[3:],
                              ExponentialSmoothing(series,trend="add").fit(smoothing_level = alpha,smoothing_slope = beta).predict(3,series.size-1))

# the function below allows you to construct a dataframe of alpha-beta combinations
def expand_grid(dictionary):
   return pd.DataFrame([row for row in product(*dictionary.values())], 
                       columns=dictionary.keys())

# define the alpha and beta values to try as a dictionary
dictionary = {'alpha': np.arange(0.0, 1.1, 0.1), 
              'beta': np.arange(0.0, 1.1, 0.1)}

# predict curve by curve
for row_number in it.chain(np.arange(0,10),np.arange(11,13)):
    # take out a censored curve, drop nan values
    temp = df_des.iloc[row_number,:].dropna().reset_index(drop=True)
    
    # convert cumulative booking into hourly sales
    temp = np.append(temp[0],temp[1:].values - temp[:-1].values)
    
    # construct alpha,beta values to try 
    des_results = expand_grid(dictionary)
    
    # add a column called mse, as a place holder for putting in the MSE results later
    des_results["mse"] = np.repeat(0,len(des_results))
    
    # reuse the DESMSE function above to cycle through all alpha beta values.
    for alpha in np.arange(0.0, 1.1, 0.1):
        for beta in np.arange(0.0, 1.1, 0.1):
           des_results.loc[(des_results["alpha"] == alpha) & (des_results["beta"] == beta),"mse"] = DESMSE(alpha,beta,temp)
    
    # find the best alpha beta: sort and put on row 1
    des_results = des_results.sort_values("mse")
    
    # use the best alpha,beta to forecast for the censored days
    # post results onto df_des
    predicted_daily_arrival = ExponentialSmoothing(temp,trend="add"). \
                                         fit(smoothing_level = des_results.iloc[0,0],
                                             smoothing_slope = des_results.iloc[0,1]). \
                                         forecast(16-temp.size)
                                        
    df_des.iloc[row_number,temp.size:] = predicted_daily_arrival.cumsum() + df_des.iloc[row_number,temp.size-1]
    


#Averaging Method
df_grocery1 = pd.read_excel('grocery_data.xlsx')
df_grocery1 = df_grocery1.iloc[1:,:16]

# rename columns
df_grocery1.columns = np.arange(1,17)
df_avg = np.cumsum(df_grocery1,axis=1)

# fill null values with 40
df_avg = df_avg.fillna(40)

# convert dataframe from 'wide' to 'long'
df_avg = pd.melt(df_avg.reset_index(),id_vars='index',var_name = 'hour',value_name='sales')
    

# sort by curve and hour
df_avg = df_avg.sort_values(by=['index','hour'])


# if 'sale' = 40, then it is censored
df_avg['censor'] = df_avg.sales == 40  


    
# hourly sales
df_avg['hourly_sale'] = df_avg.groupby('index').sales.diff()
df_avg.loc[pd.isnull(df_avg.hourly_sale),'hourly_sale'] = df_avg.loc[pd.isnull(df_avg.hourly_sale),'sales']




temp1 = df_avg[df_avg.censor==False].groupby('hour').hourly_sale.mean()
temp1 = temp1.reset_index().rename(columns = {'index' : "hour", 'hourly_sale' : 'hourly_sale_avg'})

# add the hourly sale avg column to df_avg using pd.merge
temp1['hour'] = temp1.hour.astype('object')
df_avg = pd.merge(df_avg,temp1,how='left',on='hour')


df_avg.loc[df_avg.censor,'hourly_sale'] = df_avg.loc[df_avg.censor,['hourly_sale','hourly_sale_avg']].max(axis=1)

# update sale by accumulating the updated hourly sales
df_avg['sales'] = df_avg.groupby('index').hourly_sale.cumsum()

# post results to the df
df_grocery1['avg'] = df_avg.groupby('index').sales.tail(1).values.round()


    

#Propotional Method
import pandas as pd
import numpy as np

df_booking = pd.read_excel('booking_data.xlsx')

#remove first row and column
df_booking = df_booking.iloc[1:,1:]

#rename columns
df_booking.columns = np.arange(1,41)

#replace 25 with null
df_booking = df_booking.replace(25,np.nan)

# check at which hour the demand becomes censored
df_count1 = df_booking.count(axis=1)

# find the daily demand
df_diff = df_booking.diff(axis=1)
df_diff = df_diff.replace(np.nan,0)

#step2: hourly demand to cumulative demand ratio (r) 
df_ratios = round(df_diff/ df_booking,3)

#step3: calculate the average ratios for each hour
df_average_ratios = np.nanmean(df_ratios, axis=0).round(3)

#step4: calculate R (cumulative/total) and Q (hourly/total)
array_R = np.ones(len(df_average_ratios))
array_Q = np.ones(len(df_average_ratios))
array_Q[39] = df_average_ratios[39]*array_R[39]

# calculate the R and Q backwardly
# remember that numpy array index starts from 0. so index = 15 is for hour = 16
for j in range(len(df_average_ratios)-2,-1,-1): 
    array_R[j] = array_R[j+1] - array_Q[j+1]
    array_Q[j] = array_R[j]*df_average_ratios[j]

#step5: unconstrained total demand = last unconstrainted cumulative demand / R ratio
# modify the df_count1 series to indicate the position of last unconstrained cum. demand
df_booking['position'] = df_count1

#extract last cumulative demand using the diagonal trick
df_booking['last_cum_demand'] = np.diag(df_booking.iloc[:,df_booking.position-1])

#R ratio for the position
df_booking['R'] = array_R[df_booking.position-1]

#unconstrained total demand by proportional method
df_booking['prop'] = np.ceil(df_booking['last_cum_demand']/df_booking['R'])
