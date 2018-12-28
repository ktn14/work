#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov 29 10:57:19 2018

@author: bryceshay
"""

import pandas as pd
import numpy as np
retail_dataset = pd.read_sas('durdata1_final.sas7bdat', format = 'sas7bdat', encoding='iso-8859-1')
retail_dataset['TRANSACTION_DATE']=pd.to_datetime(retail_dataset['TRANSACTION_DATE'].str[:9],format='%d%b%Y')


retail_dataset['PRODUCT_ID'].value_counts()

#Choose product and starting to clean
product_2=retail_dataset[retail_dataset['PRODUCT_ID']==758034.0]
direct=product_2[['HOUSEHOLD_ID','PRODUCT_ID','UNIT_PRICE','QUANTITY','TRANSACTION_DATE','TRANSACTION_TYPE']]
direct=direct.sort_values('TRANSACTION_DATE')
direct.reset_index(drop=True,inplace=True)
direct['difference_days']=(direct.TRANSACTION_DATE - direct.TRANSACTION_DATE[0]).dt.days


#Putting them into bins 
direct['Life_Cycle']=direct['difference_days']


def life(data):
    count=0    
    if data==0 :
        return 1
    else:
        for i in range(0,data,30):
            count+=1
        return count 

direct['Life_Cycle']=direct['Life_Cycle'].apply(life)

direct['UNIT_PRICE'].value_counts()

#Flagging the discounts
direct['discounted']=direct['UNIT_PRICE']
 
direct['discounted'][direct['discounted'] < 239.99]=1
direct['discounted'][direct['discounted'] >= 239.99]=0
direct['discounted'].value_counts()

#Creating purchases only column
direct_purchases=direct[direct['UNIT_PRICE'] > 0]
direct_purchases['discounted'].value_counts()

sales=direct_purchases.groupby('Life_Cycle')['QUANTITY'].sum().reset_index()
avg_discount=direct_purchases.groupby(['Life_Cycle','discounted'])['UNIT_PRICE'].mean().reset_index()

#sales["QUANTITY"].plot.bar()
sales.plot.scatter(x="Life_Cycle",y="QUANTITY")

direct_purchases


import statsmodels.api as sm
model1=sm.OLS(sales['QUANTITY'],)








scoot=retail_dataset[retail_dataset['PRODUCT_ID']==726129.0]
scoot2=scoot[['HOUSEHOLD_ID','PRODUCT_ID','UNIT_PRICE','TRANSACTION_DATE','TRANSACTION_TYPE']]
scoot2.info()
scoot2['UNIT_PRICE'].value_counts()
scoot2=scoot2.sort_values('TRANSACTION_DATE')
scoot2.reset_index(drop=True,inplace=True)
scoot2['difference_days']=(scoot2.TRANSACTION_DATE - scoot2.TRANSACTION_DATE[0]).dt.days



scoot2.info()
scoot2['Life_Cycle']=scoot2['difference_days']
scoot2['Life_Cycle'][scoot2['Life_Cycle'] < 443] = 1
scoot2['Life_Cycle'][(scoot2['Life_Cycle'] >= 443) & (scoot2['Life_Cycle'] < 886)] = 2
scoot2['Life_Cycle'][scoot2['Life_Cycle'] >= 886] = 3

#sort by transaction date
#weekly 

scoot_returns=scoot2[scoot2['TRANSACTION_TYPE']== 2]
scoot_returns.reset_index(drop=True,inplace=True)

scoot_purchases=scoot2[(scoot2['TRANSACTION_TYPE'] != 2) & (scoot2['UNIT_PRICE']> 5)]
scoot_purchases.reset_index(drop=True,inplace=True)

%matplotlib
import matplotlib.pyplot as plt
plt.plot_date(scoot_purchases['TRANSACTION_DATE'], scoot_purchases['UNIT_PRICE'])

import statsmodels.api as sm







discount variable, life cycle variable=how sales pattern change in the lifecycle (introduce a square term), google how to capture quadratic effect. 
product term between discount between discount and lifestyle variable. how 
pricing module 

sales = .01 * discount + 


retail_dataset['CAT_MOBILE'] = retail_dataset['CATEGORY_DESCRIPTION']
retail_dataset['CAT_MOBILE'][retail_dataset['CAT_MOBILE'] == 'MOBILE']=1
retail_dataset['CAT_MOBILE'][retail_dataset['CAT_MOBILE'] != 'MOBILE']=0
retail_dataset['CAT_DVS'][direct['CATEGORY_DESCRIPTION'] == 'DVS']=1
retail_dataset['CAT_AUDIO'][direct['CATEGORY_DESCRIPTION'] == 'AUDIO']=1


