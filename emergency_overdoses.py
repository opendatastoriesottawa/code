
# coding: utf-8

# In[ ]:


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

get_ipython().magic('matplotlib inline')


# In[ ]:


df = pd.read_excel("emergency_room_overdoses.xlsx")


# In[ ]:


df.head()


# In[ ]:


df.info()


# In[ ]:


#data counts
df.count()


# In[ ]:


#106 weeks covered - perhaps this should be divided into months, and years
df['year'] = df['Week starting on'].dt.year
df['month'] = df['Week starting on'].dt.month


# In[ ]:


df.head()


# In[ ]:


df.groupby('year')['year'].nunique()


# In[ ]:


#lets see what months we got here
df.groupby(['year','month'])['year'].max()


# In[ ]:


#okay, not a lot of data from 2015, but since then we are good
#lets summarize the data into new dataframes for years and months

df_sum = df.groupby(['year','month'])['Weekly count'].sum().reset_index()


# In[ ]:


df_sum.rename(columns={'Weekly count' : 'mthSum'}, inplace=True)
df_sum.head()


# In[ ]:


#now we will take a sum of the weeks available in each month, for general purposes
df_wksum = df.groupby(['year','month']).count().reset_index()


# In[ ]:


df_wksum.rename(columns={'Weekly count' : 'wkCnt'}, inplace=True)
df_wksum.drop(['Week starting on'],axis=1, inplace=True)
df_wksum.head()


# In[ ]:


# join the weeksum to the summary data
df_sum = pd.merge(left=df_sum, right=df_wksum, left_on=['year','month'], right_on=['year','month'], how='inner')


# In[ ]:


#let's get the index location of months with limited weeks
df_sum


# In[ ]:


#okay index locations at 0 and 25
df_sum.drop(df_sum.index[[0,25]],axis=0,inplace=True)
df_sum.head()


# In[ ]:


#lets find out about this data!
df_sum['yr_mth'] = df_sum[['year','month']].dot([100,1])
df_sum['avg_mth'] = df_sum['mthSum']/df_sum['wkCnt']
#set up figure
fig, ax = plt.subplots()
fig.set_size_inches(12,5)
plt.bar(df_sum.yr_mth,df_sum.mthSum,1)
plt.ylim(0, 60)
#ax.xaxis.plt.MaxNLocator(8)
ax.tick_params(direction='out', length=6, width=2, colors='r')

sns.barplot(x='yr_mth',y='avg_mth',data=df_sum, ax=ax, palette="Reds", hue='wkCnt')


# In[ ]:


fig, ax = plt.subplots(nrows=1, ncols=3)
plt.bar(df_sum.yr_mth,df_sum.mthSum,1)
sns.barplot(x='yr_mth',y='mthSum',data=df_sum, ax=ax)


# In[ ]:


df_sum.head()


# In[ ]:


#create new dataframe with year, month, and weekly average per month
df_sum_yrmth = df_sum.filter(["year", "month", "avg_mth"],axis=1)
df_sum_yrmth = df_sum_yrmth.pivot("year", "month", "avg_mth")


# In[ ]:


sns.heatmap(df_sum_yrmth,cmap="YlGnBu")

