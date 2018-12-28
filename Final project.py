

import pandas as pd

retail_dataset = pd.read_sas('durdata1_final.sas7bdat', format = 'sas7bdat', encoding='iso-8859-1')
retail_dataset['TRANSACTION_DATE']=pd.to_datetime(retail_dataset['TRANSACTION_DATE'].str[:9],format='%d%b%Y')


#Count the product IDs under the 'MUSIC' category and select top 3 most sold products
K = retail_dataset[retail_dataset['CATEGORY_DESCRIPTION']=='MUSIC']
K['PRODUCT_ID'].value_counts()

#Seperate first product into Df sorted by transaction date
games=retail_dataset[retail_dataset['PRODUCT_ID']==808789][['SUB_CATEGORY_DESCRIPTION','CATEGORY_DESCRIPTION','UNIT_PRICE','QUANTITY','TRANSACTION_DATE','TRANSACTION_TYPE']]
games=games.sort_values('TRANSACTION_DATE')
games.reset_index(drop=True,inplace=True)

#calculate the difference in days from beginning to end of product's life cycle
games['difference_days']=(games.TRANSACTION_DATE - games.TRANSACTION_DATE[0]).dt.days

#placed life cycle into bins by week
games['Life_Cycle']=games['difference_days']

def life(data):
    count=0    
    if data==0 :
        return 1
    else:
        for i in range(0,data,7):
            count+=1
        return count 

games['Life_Cycle']=games['Life_Cycle'].apply(life)



#Flagging the discounts by using the mode as anchor price
games['UNIT_PRICE'].mode()
games['discounted']=games['UNIT_PRICE']
 


#anything less than anchor price is flagged as discount (1)
games['discounted'][games['discounted'] < 199.99]=1
games['discounted'][games['discounted'] >= 199.99]=0
games['discounted'].value_counts()

#####filtered out returns
games=games[games['UNIT_PRICE'] > 0]
games['discounted'].value_counts()

#Sum of sales in each "bin" aka Life_Cycle
games_sales=games.groupby('Life_Cycle')['QUANTITY'].sum().reset_index()

#Average discount of each bin
avg_discount_games=games.groupby(['Life_Cycle'])['UNIT_PRICE'].mean().reset_index()
rounded_games=round(avg_discount_games['UNIT_PRICE'],2)
avg_discount_games['UNIT_PRICE']=rounded_games

#created anchor price column based on mode
avg_discount_games['anchor_price'] = 199.99



#calculated average discount percentage in each bin
avg_discount_games['average_discount_bin']=avg_discount_games['UNIT_PRICE']
product_mode=games['UNIT_PRICE'].mode()
def discount(price):
   return (product_mode - price) / product_mode
avg_discount_games['average_discount_bin']=avg_discount_games['average_discount_bin'].apply(discount)

avg_discount_games.drop(['UNIT_PRICE'],axis=1,inplace=True)

#created discount_life column by multiplying average discount by life cycle
avg_discount_games['discount_life']=avg_discount_games['average_discount_bin']*avg_discount_games['Life_Cycle']

#created squared column by squaring life cycle
avg_discount_games['squared']=avg_discount_games['Life_Cycle']**2



#Repeated same process as above on next two highest selling products
games1=retail_dataset[retail_dataset['PRODUCT_ID']==793161][['SUB_CATEGORY_DESCRIPTION','CATEGORY_DESCRIPTION','UNIT_PRICE','QUANTITY','TRANSACTION_DATE','TRANSACTION_TYPE']]
games1=games1.sort_values('TRANSACTION_DATE')
games1.reset_index(drop=True,inplace=True)
games1['difference_days']=(games1.TRANSACTION_DATE - games1.TRANSACTION_DATE[0]).dt.days

games1['Life_Cycle']=games1['difference_days']

def life(data):
    count=0    
    if data==0 :
        return 1
    else:
        for i in range(0,data,7):
            count+=1
        return count 

games1['Life_Cycle']=games1['Life_Cycle'].apply(life)
games1['UNIT_PRICE'].mode()

games1['discounted']=games1['UNIT_PRICE']

games1['discounted'][games1['discounted'] < 299.99]=1
games1['discounted'][games1['discounted'] >= 299.99]=0
games1['discounted'].value_counts()

games1=games1[games1['UNIT_PRICE'] > 0]
games1['discounted'].value_counts()

games1_sales=games1.groupby('Life_Cycle')['QUANTITY'].sum().reset_index()

avg_discount_games1=games1.groupby(['Life_Cycle'])['UNIT_PRICE'].mean().reset_index()
rounded_games1=round(avg_discount_games1['UNIT_PRICE'],2)
avg_discount_games1['UNIT_PRICE']=rounded_games1
avg_discount_games1['anchor_price'] = 299.99

avg_discount_games1['average_discount_bin']=avg_discount_games1['UNIT_PRICE']

product_mode=games1['UNIT_PRICE'].mode()
def discount(price):
   return (product_mode - price) / product_mode

avg_discount_games1['average_discount_bin']=avg_discount_games1['average_discount_bin'].apply(discount)
avg_discount_games1.drop(['UNIT_PRICE'],axis=1,inplace=True)
avg_discount_games1['discount_life']=avg_discount_games1['average_discount_bin']*avg_discount_games1['Life_Cycle']
avg_discount_games1['squared']=avg_discount_games1['Life_Cycle']**2


games2=retail_dataset[retail_dataset['PRODUCT_ID']==746200][['SUB_CATEGORY_DESCRIPTION','CATEGORY_DESCRIPTION','UNIT_PRICE','QUANTITY','TRANSACTION_DATE','TRANSACTION_TYPE']]
games2=games2.sort_values('TRANSACTION_DATE')
games2.reset_index(drop=True,inplace=True)
games2['difference_days']=(games2.TRANSACTION_DATE - games2.TRANSACTION_DATE[0]).dt.days

games2['Life_Cycle']=games2['difference_days']

def life(data):
    count=0    
    if data==0 :
        return 1
    else:
        for i in range(0,data,7):
            count+=1
        return count 

games2['Life_Cycle']=games2['Life_Cycle'].apply(life)
games2['UNIT_PRICE'].mode()

games2['discounted']=games2['UNIT_PRICE']
 
games2['discounted'][games2['discounted'] < 299.99]=1
games2['discounted'][games2['discounted'] >= 299.99]=0
games2['discounted'].value_counts()

games2=games2[games2['UNIT_PRICE'] > 0]
games2['discounted'].value_counts()

games2_sales=games2.groupby('Life_Cycle')['QUANTITY'].sum().reset_index()

avg_discount_games2=games2.groupby(['Life_Cycle'])['UNIT_PRICE'].mean().reset_index()
rounded_games2=round(avg_discount_games2['UNIT_PRICE'],2)
avg_discount_games2['UNIT_PRICE']=rounded_games2
avg_discount_games2['anchor_price'] = 299.99

avg_discount_games2['average_discount_bin']=avg_discount_games2['UNIT_PRICE']

product_mode=games2['UNIT_PRICE'].mode()
def discount(price):
   return (product_mode - price) / product_mode

avg_discount_games2['average_discount_bin']=avg_discount_games2['average_discount_bin'].apply(discount)
avg_discount_games2.drop(['UNIT_PRICE'],axis=1,inplace=True)
avg_discount_games2['discount_life']=avg_discount_games2['average_discount_bin']*avg_discount_games2['Life_Cycle']
avg_discount_games2['squared']=avg_discount_games2['Life_Cycle']**2



#Fit the model to data
##dependent variable = "Quantity" or Sales
###Independent variables = average discount per lifecycle/bin, Life cycle, squared, anchor price



import statsmodels.api as sm
product_data = pd.concat([avg_discount_games,avg_discount_games1,avg_discount_games2])
product_data.reset_index(drop=True,inplace=True)
sales_data = pd.concat([games_sales,games1_sales,games2_sales])
sales_data.reset_index(drop=True,inplace=True)


#studying the impact of discount
X=sm.add_constant(product_data[['average_discount_bin','Life_Cycle','discount_life','anchor_price']])
model=sm.OLS(sales_data['QUANTITY'],X).fit()
model.summary()


#studying the sales trajectory along the life cycle:
X2=sm.add_constant(product_data[['average_discount_bin','Life_Cycle','squared','anchor_price']])
model2=sm.OLS(sales_data['QUANTITY'],X2).fit()
model2.summary()



