# -*- coding: utf-8 -*-
"""
Created on Thu Nov 15 12:43:49 2018

@author: ktn14
"""

import pandas as pd
df = pd.read_table('C:\\Users\\ktn14\\Downloads\\amazon_labelled.txt', sep='\t',names = ['text','sentiment'])
s = df['text'][26]

import nltk
from nltk.tokenize import word_tokenize
nltk.download('punkt')

sTokenized = word_tokenize(s)
split = s.split()



def contraction(word):
    if word == "'ve":
        return 'have'
    if word == 's':
        return 'is'
    else:
        return word




s2 = []    
for i in sTokenized:
    s2.append(contraction(i))
sTokenized = s2

for i in sTokenized:
    if i.isalpha() == False:
        sTokenized.remove(i)

s3 = []
for i in sTokenized:
  s3.append(i.lower())
sTokenized = s3
 
from nltk.stem import PorterStemmer 
from nltk.corpus import stopwords
ps=PorterStemmer()
stopWords = stopwords.words('english')
nltk.download('stopwords')   

s4 = [word for word in sTokenized if word not in stopwords.words('english')]
sTokenized = s4

s5 = []
for i in sTokenized:
    s5.append(ps.stem(i))
sTokenized = s5
     

print(sTokenized)
#Q1: 7 words   


from sklearn.feature_extraction.text import CountVectorizer
analyzer = CountVectorizer().build_analyzer()
df['text'].apply(analyzer)

def Analyze(doc):
    return [ps.stem(word) for word in analyzer(doc) if word not in stopWords and word.isalpha()]

cv=CountVectorizer(analyzer=Analyze)
print(cv.fit_transform(df['text']))
print(cv.get_feature_names())

df2 =cv.fit_transform(df['text'])
count_vect_df = pd.DataFrame(df2.todense(),columns=cv.get_feature_names())

from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_score, recall_score
train_X, test_X,train_y,test_y = train_test_split(count_vect_df,df['sentiment'],test_size=0.3,random_state=42)


from sklearn import tree,svm
modelDT=tree.DecisionTreeClassifier(criterion='entropy')
modelDT.fit(train_X,train_y)
predictDT=modelDT.predict(test_X)


modelSVM=svm.SVC(kernel='linear')
modelSVM.fit(train_X,train_y)
predictSVM=modelSVM.predict(test_X)

accDict={}
accDict['DT']=accuracy_score(test_y,predictDT)
accDict['SVM']=accuracy_score(test_y,predictSVM)
precDict={}
precDict['DT']=precision_score(test_y,predictDT)
precDict['SVM']=precision_score(test_y,predictSVM)
recallDict={}
recallDict['DT']=recall_score(test_y,predictDT)
recallDict['SVM']=recall_score(test_y,predictSVM)

perfDict= {'accuracy':accDict,'precision':precDict,'recall':recallDict}
performance =pd.DataFrame.from_dict(perfDict)

print(performance)
#     accuracy  precision    recall
#DT   0.770000   0.777778  0.772727
#SVM  0.796667   0.812081  0.785714


from nltk.sentiment.vader import SentimentIntensityAnalyzer
sid = SentimentIntensityAnalyzer()
nltk.download('vader_lexicon')

pos = []
for sentence in df['text']:
    pos.append(sid.polarity_scores(sentence)['pos'])
    
neg = []
for sentence in df['text']:
    neg.append(sid.polarity_scores(sentence)['neg'])
    
df2 = pd.DataFrame({'pos':pos,'neg':neg})

def sentiment(df,i):
    if df.iloc[i][0] > df.iloc[i][1]:
        return 1 
    else:
        return 0
    
value = []
for i in range (df2.shape[0]):
    value.append(sentiment(df2,i))
df2['newS'] = value 
 
from sklearn.metrics import accuracy_score
accuracy = accuracy_score(df['sentiment'],df2['newS'])
print(accuracy)
#83.2%    

