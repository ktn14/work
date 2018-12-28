# -*- coding: utf-8 -*-
"""
Created on Thu Oct 25 12:32:07 2018

@author: ktn14
"""

import pandas as pd
df = pd.read_csv('C:\\Users\\ktn14\\Downloads\\SPSS_cars_v2.csv')

import matplotlib.pyplot as plt


#Q1
dfHistogram = df[df.mpg.notnull()]
dfMpg = dfHistogram[['mpg','country']]
sMpg = dfMpg[dfMpg.country == 'Sweden']
UMpg = dfMpg[dfMpg.country == 'United States']
GMpg = dfMpg[dfMpg.country == 'Germany']
JMpg = dfMpg[dfMpg.country == 'Japan']


fig1 = plt.figure()
ax1 = fig1.add_subplot(2,2,1)
ax2 = fig1.add_subplot(2,2,2)
ax3 = fig1.add_subplot(2,2,3)
ax4 = fig1.add_subplot(2,2,4)


ax1.hist(sMpg['mpg'], bins=5)
ax1.set_title('Sweden')

ax2.hist(UMpg['mpg'], bins=5)
ax2.set_title('United States')

ax3.hist(GMpg['mpg'], bins=5)
ax3.set_title('Germany')

ax4.hist(JMpg['mpg'], bins=5)
ax4.set_title('Japan')

fig1.tight_layout()


#Q2
fig2 =plt.figure()
ax1 = fig2.add_subplot(2,2,1)
ax2 = fig2.add_subplot(2,2,2)
ax3 = fig2.add_subplot(2,2,3)
ax4 = fig2.add_subplot(2,2,4)



price = df.dropna(subset = ['price'])
sales = df.dropna(subset = ['sales'])
resale = df.dropna(subset =['resale'])
horsepow = df.dropna(subset = ['horsepow'])

priceList = [price.loc[price['country']=='Sweden','price',],price.loc[price['country'] == 'United States', 'price'],price.loc[price['country'] == 'Japan', 'price'],price.loc[price['country'] == 'Germany', 'price']]
salesList = [sales.loc[sales['country']=='Sweden','sales',],sales.loc[sales['country'] == 'United States', 'sales'],sales.loc[sales['country'] == 'Japan', 'sales'],sales.loc[sales['country'] == 'Germany', 'sales']]
resaleList = [resale.loc[resale['country']=='Sweden','resale',],resale.loc[resale['country'] == 'United States', 'resale'],resale.loc[resale['country'] == 'Japan', 'resale'],resale.loc[resale['country'] == 'Germany', 'resale']]
hpList = [horsepow.loc[horsepow['country']=='Sweden','horsepow',],horsepow.loc[horsepow['country'] == 'United States', 'horsepow'],horsepow.loc[horsepow['country'] == 'Japan', 'horsepow'],horsepow.loc[horsepow['country'] == 'Germany', 'horsepow']]




ax1.boxplot(priceList, labels = ['Sweden','Japan', 'US', 'Germany'])
ax1.set_ylabel('price')
ax1.set_xlabel('country')
ax1.set_title('Price')

ax2.boxplot(salesList, labels = ['Sweden','Japan', 'US', 'Germany'])
ax2.set_ylabel('sales')
ax2.set_xlabel('country')
ax2.set_title('Sales')

ax3.boxplot(resaleList, labels = ['Sweden','Japan', 'US', 'Germany'])
ax3.set_ylabel('resale')
ax3.set_xlabel('country')
ax3.set_title('Resale')

ax4.boxplot(hpList, labels = ['Sweden','Japan', 'US', 'Germany'])
ax4.set_ylabel('horsepower')
ax4.set_xlabel('country')
ax4.set_title('Horsepower')

fig2.tight_layout()








#Q3
fig3 = plt.figure()
ax3 = fig3.add_subplot(2,2,1)
ax3.scatter(df['width'][df.country == 'Sweden'],df['length'][df.country == 'Sweden'])
ax3.set_title('Sweden')
ax3.set_xlabel('width')
ax3.set_ylabel('Length')

ax3 = fig3.add_subplot(2,2,2)
ax3.scatter(df['width'][df.country == 'Japan'],df['length'][df.country == 'Japan'])
ax3.set_title('Japan')
ax3.set_xlabel('width')
ax3.set_ylabel('Length')


ax3 = fig3.add_subplot(2,2,3)
ax3.scatter(df['width'][df.country == 'United States'],df['length'][df.country == 'United States'])
ax3.set_title('US')
ax3.set_xlabel('width')
ax3.set_ylabel('Length')


ax3 = fig3.add_subplot(2,2,4)
ax3.scatter(df['width'][df.country == 'Germany'],df['length'][df.country == 'Germany'])
ax3.set_title('Germany')
ax3.set_xlabel('width')
ax3.set_ylabel('Length')

fig3.tight_layout()


#Q4
obsByModel = df['manufact'][df['country'] == 'United States'].value_counts()
axes = obsByModel.plot(kind = 'bar', color = 'red', alpha =0.7)


#Q5
fig5 = plt.figure()
ax5 = fig5.add_subplot(1,1,1)
manufact = df.dropna(subset = ['manufact'])
manufact['c/m'] = manufact['country'].map(str) + ' / ' + manufact['manufact']
manufact = manufact.groupby('c/m')['c/m'].count()

ax5.bar(range(manufact.shape[0]), manufact.values, color = 'red', alpha = 0.7, tick_label = manufact.index)
ax5.set_title('Manufacturer')
ax5.set_xlabel('Manufacturer')
ax5.set_ylabel('Number of Cars')
plt.xticks(rotation = 90)
fig5.tight_layout()


#Q6

a = df[['manufact', 'sales']][df['country'] == 'Japan']
b = a.groupby('manufact')['sales'].sum()
labels = 'Acura', 'Honda','Lexus', 'Toyota', 'Nissan', 'Mitsubishi'

fig6 = plt.figure()
ax6 = fig6.add_subplot(1,1,1)
ax6.pie(b, labels=labels, autopct='%1.1f%%', shadow=True, startangle=140 )
plt.axis('equal')
plt.show()


