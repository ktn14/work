# -*- coding: utf-8 -*-

"""
Created on Sun Oct 21 14:39:32 2018

@author: ktn14
"""


#Step1
import pandas as pd
df1 = pd.read_csv('C:\\Users\\ktn14\\Downloads\\expedia_clicks.csv')
df2 = pd.read_csv('C:\\Users\\ktn14\\Downloads\\expedia_properties.csv')


dfMerged = pd.merge(df1,df2,how='inner',on='prop_id')


dfMerged.drop_duplicates(subset=['srch_id'],keep='first',inplace=True)
dfMerged.describe(include='all')


#Step2 
dfMerged['QuarterYear'] = pd.PeriodIndex(dfMerged.date_time, freq='Q')



dfMerged['quarter year'] = dfMerged['date_time']
dfMerged['day_time'] =  pd.to_datetime(dfMerged['date_time'])
dfMerged['day_time'] = dfMerged.day_time.apply(lambda x: x.hour)


def time_period(time):
    if 5 <= time < 12:
        return 'Morning'
    elif 12 <= time < 17:
        return 'Afternoon'
    elif 17 <= time < 22:
        return 'Evening'
    else:
        return 'Night'
dfMerged['period_time'] = dfMerged['day_time'].apply(time_period)


dfMerged['AdditionalCharges'] = (dfMerged['gross_booking_usd'] - (dfMerged['price_usd'] * dfMerged['srch_length_of_stay'])) / (dfMerged['price_usd'] * dfMerged['srch_length_of_stay'])

def booking(row):
    if row['visitor_location_country_id'] == row['prop_country_id']:
        return 'domestic'
    if row['visitor_location_country_id'] != row['prop_country_id']:
        return 'international'
dfMerged['planned booking'] = dfMerged.apply(booking, axis = 1)



def score(row):
    if row['prop_review_score'] < 4:
        return 'low'
    else:
        return 'high'
dfMerged['review_score_bin']= dfMerged.apply(score, axis=1)


#Step3
#Q1
dfMerged.groupby('QuarterYear', as_index=False)['gross_booking_usd'].sum()
#highest during Q2 2013

#Q2
dfMerged.groupby('period_time')['booking_bol'].sum()
#Afternoon: 2020
#Evening: 1864
#Morning: 2090
#Night: 661


#Q3
dfMerged.groupby(['planned booking', 'review_score_bin'])['srch_length_of_stay'].mean()
#domestic         high                1.789912
#                 low                 1.837583
#international    high                2.661629
#                 low                 2.476368

#Q4 
Q4 =dfMerged.groupby('prop_country_id', as_index=False)['AdditionalCharges'].mean()
#224