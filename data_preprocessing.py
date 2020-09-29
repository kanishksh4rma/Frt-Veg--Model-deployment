# -*- Code for Data Preproceesing & Feature Engineering -*-
# ---------------------------------------------------------

# import data and libraries 

import pandas as pd
import numpy as np

df = pd.read_excel('/content/BQ-Assignment-Data-Analytics.xlsx')

# ---------------------------------------
# convert date to month names and remove date

import calendar
df.Date = df.Date.apply(lambda x: str(calendar.month_abbr[x.month])+' 20')
all_col = list(df.columns)
all_col.remove('Item')
dd = df.groupby('Date')[all_col].sum()

date_order = dd.index
date_order.unique()

for i in df.Date.unique():
  df[i] = 0
  df.loc[df['Date'] == i, i] = df.loc[df['Date'] == i, 'Sales']

df.drop(['Date','Sales'],inplace=True,axis=1)

# ---------------------------------------
# add Item Sort Order to DataFrame
all_col=[]
all_col.append('Item Sort Order')
for i in date_order.unique():
  all_col.append(i)

df['Item Sort Order'].astype(int)
gp_by_data = df.groupby('Item')[all_col].sum()


sort_order = df.groupby('Item')['Item Sort Order'].unique()
sort_order_df = pd.DataFrame(sort_order,columns = ['Item Sort Order'])
sort_order_df['Item Sort Order'] = sort_order_df['Item Sort Order'].apply(lambda x: str(x).replace('[','') )  # remove unnecessary characters
sort_order_df['Item Sort Order'] = sort_order_df['Item Sort Order'].apply(lambda x:str(x).replace(']','') )   # remove unnecessary characters
gp_by_data['Item Sort Order'] = sort_order_df['Item Sort Order']

# ---------------------------------------
# add Item Type to DataFrame

gg = df.groupby('Item')['Item Type'].unique()
gg = pd.DataFrame(gg,columns=['Item Type'])
gg['Item Type'] = gg['Item Type'].apply(lambda x: str(x).replace("[","") )  # remove unnecessary characters
gg['Item Type'] = gg['Item Type'].apply(lambda x:str(x).replace("]","") )   # remove unnecessary characters
gg['Item Type'] = gg['Item Type'].apply(lambda x:str(x).replace("'","") )   # remove unnecessary characters
gg['Item Type'] = gg['Item Type'].apply(lambda x:str(x).replace("'","") )   # remove unnecessary characters

gp_by_data['Item Type'] = gg

gp_by_data.to_excel('cleaned2.xlsx')