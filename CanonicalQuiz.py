# -*- coding: utf-8 -*-
"""
Created on Tue Nov  6 17:24:39 2018

@author: ktn14
"""
#In Class Exercise 1



import statsmodels.formula.api as smf
import pandas as pd
dfD = pd.read_csv("demand_data.csv")


weekendFit = smf.ols(formula='demand ~ price + weekend', data=dfD).fit()
weekendFit.summary()
weekendFit.params



from scipy.optimize import minimize_scalar
pi =lambda x: -(weekendFit.params[0] + weekendFit.params[1]*x + weekendFit.params[2]) * (x-3)  
minimize_scalar(pi, method='brent')



#In Class Exercise 2
dfR = pd.read_csv('refurb_data.csv')
dfR['dates'] = pd.to_datetime(dfR['dates'])
dfR.info()
dfR.head(10)

import matplotlib.pyplot as plt
plt.figure(figsize=(8,5))
plt.plot(dfR.iloc[:,:-1].drop_duplicates().dates,
         dfR.iloc[:,:-1].drop_duplicates().new_price, label='New Product Price')
plt.plot(dfR.iloc[:,:-1].drop_duplicates().dates,
         dfR.iloc[:,:-1].drop_duplicates().refurb_price, label='Refurbished Product Price')
plt.legend(loc='best')
plt.xlabel('Date')
plt.ylabel('Price')
plt.show()



demandR = dfR[dfR['choice'] == 'refurb'].groupby('dates')['choice'].count()
demandNew = dfR[dfR['choice'] == 'new'].groupby('dates')['choice'].count()
newpriceDaily = dfR[dfR['choice'] == 'new'].groupby('dates')['new_price'].max()
refpriceDaily = dfR[dfR['choice'] == 'refurb'].groupby('dates')['refurb_price'].max()
demandDaily = pd.concat([demandNew, demandR, newpriceDaily, refpriceDaily], axis = 1)
demandDaily.columns = ['new_demand', 'refurb_demand', 'new_price', 'refurb_price']
demandDaily['new_p'] = demandDaily['new_price'] * demandDaily['new_demand']

import statsmodels.formula.api as smf
refurbFit = smf.ols(formula = 'refurb_demand ~ new_price + refurb_price', data = demandDaily).fit()
refurbFit.summary()
refurbFit.params

from scipy.optimize import minimize_scalar
pi =lambda x: -(refurbFit.params[0] + refurbFit.params[1]*350 + refurbFit.params[2]*x) * (x-150)  
minimize_scalar(pi, method='brent')
