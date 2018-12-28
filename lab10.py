# -*- coding: utf-8 -*-
"""
Created on Thu Nov 29 12:35:48 2018

@author: ktn14
"""
import pandas as pd
with open ("fraudulent_emails.txt", 'r', errors='ignore') as file:
    df1 = file.read()
    
import re 
exp = re.compile(r'.*From: "(?i)dr\.?\s?.*')
matches = re.findall(exp,df1)
x = []
for i in matches: 
    split = i.split('"')
    x.append(split)
names = []
emails = []
domains = []
for i in x:
    name = i[1]
    email = i[2]
    email = email[2:-1]
    domain = email
    symbol = domain.find('@')
    domain = domain[-4:]
    names.append(name)
    emails.append(email)
    domains.append(domain) 
newdf = pd.DataFrame({'name':names, 'email':emails,'domain':domains})
words = ['.com', '.net']
newdf = newdf[newdf.domain.isin(words)]



 
df2 = pd.read_csv('headlines.csv')
df2.columns = ['headline']
from sklearn.feature_extraction.text import CountVectorizer
from nltk.corpus import stopwords
df3 = df2['headline']
stopWords = stopwords.words('english')
analyzer = CountVectorizer().build_analyzer()

def Analyze(text):
    return [i.lower() for i in analyzer(text) if i not in stopWords]

countVectorizer = CountVectorizer(min_df = 5, max_df = 0.8, analyzer = Analyze)
terms = countVectorizer.fit(df3)
X = terms.transform(df3)
termList = terms.get_feature_names()
dfX = pd.DataFrame(X.toarray(), columns = termList)

from sklearn.decomposition import LatentDirichletAllocation
lda = LatentDirichletAllocation(n_components = 10)
ldamod = lda.fit(dfX)
wordCounter = 15
for idx, topic in enumerate(ldamod.components_):
    sortedIndices = topic.argsort()[::-1]
    print('Topic {}: '.format(idx+1),[(termList[i]) for i in sortedIndices[:wordCounter]])









