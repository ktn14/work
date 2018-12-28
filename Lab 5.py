# -*- coding: utf-8 -*-
"""
Created on Thu Sep 27 12:35:14 2018

@author: ktn14
"""

import pandas as pd
dfTimes = pd.read_csv('C:\\Users\\ktn14\\Downloads\\FlightInfo_times.csv')
dfGeneral = pd.read_csv('C:\\Users\\ktn14\\Downloads\\FlightInfo_general.csv', delimiter = ';')

dfTimes = dfTimes.drop_duplicates('FlightID')
dfGeneral = dfGeneral.drop_duplicates('FlightID')

dfMerged = pd.merge(dfGeneral, dfTimes, on='FlightID')



def f(aNum):
    aNum = str(aNum)
    return aNum[:-2]+':'+aNum[-2:]

dfMerged['ScheduledDeptTime'] = dfMerged['ScheduledDeptTime'].apply(f)
dfMerged['ActualDeptTime'] = dfMerged['ActualDeptTime'].apply(f)

dfMerged['ScheduledDeptTime_full'] = pd.to_datetime(dfMerged.ScheduledDeptTime)
dfMerged['ActualDeptTime_full'] = pd.to_datetime(dfMerged.ActualDeptTime)

dfMerged['TimeDiff'] = dfMerged['ActualDeptTime_full']-dfMerged['ScheduledDeptTime_full'] 


dfMerged['Delayed'] = 0
def diff(time):
    if time < pd.Timedelta('20 min'):
        return dfMerged['Delayed'] == 1
    else:
        return dfMerged['Delayed'] == 0 


dfMerged['Delayed'] = dfMerged['TimeDiff'].apply(diff)
dfMerged['Delayed'].replace(True, 1, inplace = True)



dfMerged['TimeOfDay'] = 'Morning'
dfMerged['TimeOfDay'].loc[(pd.to_datetime(dfMerged['ScheduledDeptTime']) >= pd.to_datetime('12:00:00')) & (pd.to_datetime(dfMerged['ScheduledDeptTime']) < pd.to_datetime('18:00:00'))] = 'Afternoon'
dfMerged['TimeOfDay'].loc[(pd.to_datetime(dfMerged['ScheduledDeptTime']) >= pd.to_datetime('18:00:00'))] = 'Evening'

dfMerged = dfMerged[dfMerged.Carrier != 'OH']

dfMergedNew = dfMerged.drop(['FlightID', 'ScheduledDeptTime','ActualDeptTime','Date','FlightNumber','TailNumber','ScheduledDeptTime_full', 'ActualDeptTime_full', 'TimeDiff'], axis=1)

def string(aNum):
    return str(aNum)
dfMergedNew['DayOfWeek'] = dfMergedNew['DayOfWeek'].apply(string)

dfMergedNew = pd.get_dummies(data=dfMergedNew, columns = ['Carrier', 'Destination', 'Origin', 'DayOfWeek', 'TimeOfDay'])


from sklearn.model_selection import train_test_split
from sklearn.model_selection import cross_val_score
from sklearn.cross_validation import train_test_split


x_train,x_test = train_test_split(dfMergedNew, test_size=0.3,random_state=42)
xy= x_train['Delayed']
x_train.drop(['Delayed'], axis = 1, inplace = True)
y = x_test['Delayed']
x_test.drop(['Delayed'], axis =1, inplace = True)

from sklearn import tree
model = tree.DecisionTreeClassifier()
model.fit(x_train, xy)
predictions = model.predict(x_test)
from sklearn.metrics import accuracy_score
from sklearn.metrics import precision_score
from sklearn.metrics import recall_score

acc1 = accuracy_score(y,predictions).mean()
precision1 = precision_score(y ,predictions).mean()
recall1 = recall_score(y,predictions).mean()
print('acc is:', acc1)
print('precision is:', precision1)
print('recall is:', recall1)

z = dfMergedNew['Delayed']
dfMergedNew.drop(['Delayed'],axis=1,inplace = True)


acc= cross_val_score(model, dfMergedNew,z, cv=5, scoring = 'accuracy').mean()
precision = cross_val_score(model, dfMergedNew, z, cv=5, scoring = 'precision').mean()
recall = cross_val_score(model, dfMergedNew, z, cv=5, scoring = 'recall').mean()
print('acc is:', acc)
print('precision is:', precision)
print('recall is:', recall)
