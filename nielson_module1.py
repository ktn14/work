# -*- coding: utf-8 -*-
"""
Created on Tue Sep  4 17:36:31 2018

@author: ktn14
"""

import pandas as pd
dfjeans = pd.read_excel('C:\\Users\\ktn14\\downloads\\ISM\\jeans_data.xlsx')

import statsmodels.api as sm
#model 1
X = sm.add_constant(dfjeans[['price','se_indicator']])

olsjeans = sm.OLS(dfjeans.sales, X).fit()
olsjeans.summary()
olsjeans.predict([1,110,1])


#model 2
dfjeans['discount']=(135-dfjeans.price)/135
X=sm.add_constant(dfjeans[['discount','se_indicator']])
olsjeans = sm.OLS(dfjeans.sales, X).fit()
olsjeans.summary()
olsjeans.predict([1,.185,1])

