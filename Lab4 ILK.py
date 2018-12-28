# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import pandas as pd
dftrain = pd.read_csv('C:\\Users\\ktn14\\Downloads\\cc_train.csv')
dfpredict = pd.read_csv('C:\\Users\\ktn14\\Downloads\\cc_predict.csv')


dfAll = pd.concat([dftrain,dfpredict],ignore_index=True)
dfAll['car'].fillna('NO', inplace=True)
dfAll['income'].fillna((dfAll['income'].mean()), inplace=True)

dfAll.drop_duplicates(subset=['id'],keep='first', inplace=True)
dfAll.drop('id',axis=1, inplace=True)


#Age attribute: Bin the age values into 3 groups as follows: IF age < 30 then the
#value = 0; IF 30<= age < 60 then age value = 1; if age >=60 then age value = 2. 

    
dfAll['age'][dfAll['age']<30] = 0
dfAll['age'][(dfAll['age']>=30) & (dfAll['age']<60)] = 1
dfAll['age'][dfAll['age']>=60] = 2


dfAll['children'][dfAll['children']==0] =0
dfAll['children'][dfAll['children']==1] =1
dfAll['children'][dfAll['children']>=2] =2

dfAll['income']=pd.qcut(dfAll['income'],4,labels = False)

binary_list =[]
multi_list = []
for i in dfAll:
    if (dfAll[i].nunique()==2):
        binary_list.append(i)
    else:
        multi_list.append(i)

bindf = dfAll[binary_list]
multidf = dfAll[multi_list]

multidf['age'] = multidf['age'].astype(str)
multidf['income'] = multidf['income'].astype(str)
multidf['children'] = multidf['children'].astype(str)

bindf=pd.get_dummies(bindf)
multidf=pd.get_dummies(multidf)


bindf=bindf.drop(['sex_FEMALE','married_NO','car_NO','save_act_NO','current_act_NO','mortgage_NO','response_NO'],axis=1)

dfAllnew = pd.concat([bindf,multidf], axis = 1)
trainInput = dfAllnew[:600]
trainInput.drop(columns=['response_YES'],inplace = True)

trainLabel = dfAll['response'][:600]
trainLabel.replace(['YES','NO'],[1,0], inplace = True)

toPredict = dfAllnew[600:]
toPredict.drop(columns=['response_YES'],inplace = True)

    
from sklearn.naive_bayes import BernoulliNB
nb = BernoulliNB()
nb.fit(trainInput,trainLabel)
predict_val = nb.predict(toPredict)

from sklearn import tree
model = tree.DecisionTreeClassifier()
model.fit(trainInput,trainLabel)
dct = model.predict(toPredict)


import numpy as np
numMatches = np.equal(predict_val,dct)
np.sum(numMatches )

proba = nb.predict_proba(toPredict)

region = dfpredict.iloc[:,3]
dfNew = pd.DataFrame(proba[:,1],columns=['Yes'])
dfNew2 = pd.concat([dfNew,region],axis = 1)

dfNew2['region'][dfNew2['region']=='INNER_CITY'] = 10000
dfNew2['region'][dfNew2['region']=='SUBURBAN'] = 9850
dfNew2['region'][dfNew2['region']=='TOWN'] = 9200
dfNew2['region'][dfNew2['region']=='RURAL'] = 7800
dfNew2['ER']=dfNew2['region']*dfNew2['Yes']
dfNew2['ID']=dfpredict.iloc[:,0]
dfNew2.sort_values('ER',ascending =False, inplace = True)



