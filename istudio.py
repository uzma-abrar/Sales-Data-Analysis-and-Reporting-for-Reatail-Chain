#!/usr/bin/env python
# coding: utf-8

# In[2]:


import pandas as pd


# In[3]:


trxn= pd.read_csv("C:/Users/uzmaa/Downloads/Retail_Data_Transactions.csv/Retail_Data_Transactions.csv")


# In[4]:


trxn


# In[5]:


response= pd.read_csv("C:/ProgramData/MySQL/MySQL Server 8.0/Uploads/Retail_Data_Response.csv")


# In[6]:


response


# In[7]:


df= trxn.merge(response,on= 'customer_id', how= 'left')


# In[8]:


df


# In[9]:


df.dtypes
df.shape
df.head()
df.describe()


# In[10]:


df.isnull().sum()


# In[11]:


df=df.dropna()


# In[12]:


df


# In[13]:


df['trans_date'] = pd.to_datetime(df['trans_date'])
df['response']= df['response'].astype('int64')


# In[14]:


df


# In[15]:


set(df['response'])


# In[16]:


df.dtypes


# In[17]:


#check for outliers

from scipy import stats
import numpy as np


# In[18]:


#calculate z score
z_scores = np.abs(stats.zscore(df['tran_amount']))

#set a threshold

threshold=3

outliers= (z_scores>threshold)
print(df[outliers])


# In[19]:


#calculate z score
z_scores = np.abs(stats.zscore(df['response']))

#set a threshold

threshold=3

outliers= (z_scores>threshold)
print(df[outliers])


# In[20]:


import seaborn as sns
import matplotlib.pyplot as plt


# In[21]:


sns.boxplot(x=df['response'])
plt.show()


# In[22]:


sns.boxplot(x=df['tran_amount'])
plt.show()


# In[23]:


#creating new column

df['month']= df['trans_date'].dt.month


# In[24]:


df


# In[25]:


# which 3 month have had the highest transaction amount
monthly_sales = df.groupby('month')['tran_amount'].sum() 
monthly_sales= monthly_sales.sort_values(ascending= False).reset_index()
monthly_sales


# In[26]:


# customers having highest number of orders
customer_counts= df['customer_id'].value_counts().reset_index()
customer_counts.columns= ['customer_id','count']
customer_counts

#sort

top_5_cus= customer_counts.sort_values(by='count', ascending= False).head(5)
top_5_cus


# In[27]:


sns.barplot(x='customer_id', y= 'count', data= top_5_cus)


# In[28]:


# customers having highest value of orders
customer_sales= df.groupby('customer_id')['tran_amount'].sum().reset_index()
customer_sales

#sort

top_5_sal= customer_sales.sort_values(by='tran_amount', ascending= False).head(5)
top_5_sal


# In[29]:


sns.barplot(x='customer_id', y= 'tran_amount', data= top_5_sal)


# In[30]:


#TIME SERIES ANALYSIS
import matplotlib.dates as mdates
df['month_year'] = df['trans_date'].dt.to_period('M')
monthly_sales= df.groupby('month_year')['tran_amount'].sum()


monthly_sales.index = monthly_sales.index.to_timestamp()

plt.figure(figsize=(12,6))
plt.plot(monthly_sales.index,monthly_sales.values)


plt.xlabel('Month_Year')
plt.ylabel('Sales')
plt.title('Monthly_sales')

plt.show()


# In[31]:


df


# In[32]:


#COHORT SEGMENTATION

#recency
recency= df.groupby('customer_id')['trans_date'].max()

#frequency
frequency = df.groupby ('customer_id')['trans_date'].count()

#monetary
monetary = df.groupby ('customer_id')['tran_amount'].sum()

#combine
rfm= pd.DataFrame({'recency': recency,'frequency': frequency, 'monetary': monetary})


# In[33]:


rfm


# In[34]:


#customer segmentation
def segment_customer(row):
    if row['recency'].year>= 2012 and row['frequency']>=15 and row['monetary']>1000:
        return 'P0'
    elif (2011<=row['recency'].year<2012) and (10<row['frequency']<15) and (500<=row['monetary']<=1000):
        return 'P1'
    else:   
        return 'P2'

rfm['segment']= rfm.apply(segment_customer, axis = 1)


# In[35]:


rfm


# In[36]:


#CHURN ANALYSIS
 # Count the number of churned and active customers
churn_counts= df['response'].value_counts()

#Plot
churn_counts.plot(kind= 'bar')


# #Analysing Top Customers

# In[37]:


top_5_cus= monetary.sort_values(ascending=False).head(5).index

top_customers_df= df[df['customer_id'].isin(top_5_cus)]

top_customer_sales= top_customers_df.groupby(['customer_id','month_year'])['tran_amount'].sum().unstack(level=0)
top_customer_sales.plot(kind= 'line')


# In[38]:


df.to_csv('MainData.csv')


# In[39]:


rfm.to_csv('AddAnalys.csv')


# In[40]:


df.head()


# In[41]:


rfm.head()


# In[42]:


df.to_excel("Output_data.xlsx", index=False)


# In[43]:


rfm.to_excel("add_analysis.xlsx", index=False)


# In[ ]:




