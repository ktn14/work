# -*- coding: utf-8 -*-
"""
Created on Tue Sep 25 11:04:18 2018

@author: ktn14
"""


#Part 1
import pandas as pd
dfjeans = pd.read_excel("jeans_data.xlsx")
dfjeans["promo_114"] = dfjeans.price == 114.75
dfjeans["promo_101"] = dfjeans.price == 101.25
import statsmodels.api as sm
X = sm.add_constant(dfjeans[["promo_114","promo_101"]].astype("int"))
X["se_indicator"] = dfjeans.se_indicator
olsjeans = sm.OLS(dfjeans.sales, X).fit()
dfjeans["residual"] = olsjeans.resid

dfjeans["residual"].rolling(3).mean()
from sklearn.metrics import mean_squared_error
mean_squared_error(dfjeans.residual[4:25], 
                   dfjeans["residual"].rolling(3).mean()[4:25])                 

for index in range(1,6):
    print([index,mean_squared_error(dfjeans.residual[5:], 
                                    dfjeans["residual"].rolling(index).mean()[4:25])])

    
from statsmodels.tsa.api import ExponentialSmoothing
import numpy as np
for alpha in np.arange(0.0, 1.1, 0.1):
    print([alpha,
           mean_squared_error(dfjeans.residual[5:],ExponentialSmoothing(dfjeans.residual).fit(smoothing_level = alpha).predict(5,))])

    
#Part2
dfbitcoin = pd.read_pickle('bitcoin_data.pkl')

# eyeball test
dfbitcoin.plot.line(x="date",y="price")


from statsmodels.tsa.stattools import adfuller
ad_result = adfuller(dfbitcoin.price)
print('ADF Statistic: %f' % ad_result[0])
print('p-value: %f' % ad_result[1])


def DESMSE(alpha,beta):
    return mean_squared_error(dfbitcoin.price[10:150],
                              ExponentialSmoothing(dfbitcoin.price[:150],trend="add").fit(smoothing_level = alpha,smoothing_slope = beta).predict(10,149))


from itertools import product
def expand_grid(dictionary):
   return pd.DataFrame([row for row in product(*dictionary.values())], 
                       columns=dictionary.keys())

dictionary = {'alpha': np.arange(0.0, 1.05, 0.05), 
              'beta': np.arange(0.0, 1.05, 0.05)}

des_results = expand_grid(dictionary)

# add a column called mse, as a place holder for putting in the MSE results later
des_results["mse"] = np.repeat(0,len(des_results))
    
    
    
    
des_results.loc[(des_results["alpha"]==.05)&(des_results["beta"] ==.05),]

import time
start = time.time()

for alpha in np.arange(0.0, 1.05, 0.05):
    for beta in np.arange(0.0, 1.05, 0.05):
       des_results.loc[(des_results["alpha"] == alpha) & (des_results["beta"] == beta),"mse"] = DESMSE(alpha,beta)
    
end = time.time()
end-start    


des_results.sort_values("mse").head(5)

# store DES(1,0.05) in the test sample
dfbitcoin.loc[dfbitcoin.index[150:], 'des'] = ExponentialSmoothing(dfbitcoin.price[:150],trend="add").fit(smoothing_level = 1,smoothing_slope = 0.04).forecast(30)

# MSE in the holdout sample
mean_squared_error(dfbitcoin.price[150:],dfbitcoin.des[150:])

#Part 3 
# Triple ES
# load data, two issues:
# 1. month is loaded as index
# 2. convert format from wide to long
dfairline = pd.read_excel("airline_data.xlsx")
# reset index
dfairline = dfairline.reset_index()
# wide to long
dfairline = pd.melt(dfairline, id_vars=['index'])
# rename
dfairline.columns = ["month","year","load"]

# de-seasonalize series
# sample average
dfairline["avg"] = dfairline.load.dropna().mean()
# monthly average
# to do this simply, use the transform method, which is a not well understood function in python
# see this post for explanation: http://pbpython.com/pandas_transform.html
dfairline["month_avg"] = dfairline.groupby("month").load.transform("mean")
# seasonal factor
dfairline["season_factor"] = dfairline.month_avg / dfairline.avg
# de-sesonalized series
dfairline["de_load"] = dfairline.load / dfairline.season_factor
   


from statsmodels.tsa.stattools import adfuller
ad_result = adfuller(dfairline.de_load[:130])
print('ADF Statistic: %f' % ad_result[0])
print('p-value: %f' % ad_result[1])


for index in range(1,6):
    print([index,mean_squared_error(dfairline.de_load[7:130], 
                                    dfairline["de_load"].rolling(index).mean()[5:128])])

    
dfairline.loc[dfairline.index[130:],'de_load'] = dfairline['de_load'].rolling(3).mean().iloc[129]
dfairline.loc[dfairline.index[130:],'load'] = dfairline['de_load']*dfairline['season_factor']

dfairline
