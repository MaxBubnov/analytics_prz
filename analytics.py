import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import calendar
import numpy as np

df = pd.read_csv("file.csv")
df.dropna(inplace=True)
df.drop(['Unnamed: 0'], axis=1, inplace=True)

df['total'] = df['Avg_Price'] * df['Quantity'] + df['Delivery_Charges']
df['when'] = pd.to_datetime(df['Transaction_Date'])

df['monthname'] = df['Month'].apply(lambda x: calendar.month_name[int(x)] if 1 <= int(x) <= 12 else 'Unknown')

df['tenure_group'] = pd.cut(df['Tenure_Months'], bins=[0,6,12,24,100], labels=['new','6m','1y','2y+'])

plt.figure(figsize=(10,5))
sns.scatterplot(data=df, x='tenure_group', y='total', palette='pastel')
plt.title('Spending by Customer Tenure')
plt.show()

df['discount_group'] = np.where(df['Discount_pct']>0, 'with_discount', 'no_discount')

plt.figure(figsize=(12,6))
temp1 = df.groupby('monthname')['total'].sum().reindex(list(calendar.month_name)[1:])
sns.barplot(x=temp1.index, y=temp1.values, palette='viridis')
plt.xticks(rotation=45)
plt.title('Total Spend by Month')
plt.show()

plt.figure(figsize=(12,6))
temp2 = df['Product_Category'].value_counts().nlargest(10)
sns.barplot(x=temp2.values, y=temp2.index, palette='rocket')
plt.title('Top 10 Product Categories')
plt.show()

plt.figure(figsize=(10,6))
temp3 = df.groupby('Coupon_Status')['total'].mean()
sns.barplot(x=temp3.index, y=temp3.values, palette='mako')
plt.title('Average Spend by Coupon Status')
plt.show()

plt.figure(figsize=(10,6))
temp4 = df.groupby('Gender')['total'].sum()
plt.pie(temp4, labels=temp4.index, autopct='%1.1f%%', colors=['lightcoral','lightskyblue'], startangle=90)
plt.title('Spending by Gender')
plt.show()

plt.figure(figsize=(12,6))
temp5 = df['Location'].value_counts().nlargest(10)
sns.barplot(x=temp5.values, y=temp5.index, palette='flare')
plt.title('Top 10 Locations')
plt.show()

temp6 = df.groupby('monthname')[['Online_Spend','Offline_Spend']].sum().reindex(list(calendar.month_name)[1:])
temp6.plot(kind='bar', stacked=True, color=['skyblue','salmon'], figsize=(12,6))
plt.xticks(rotation=45)
plt.title('Online vs Offline Spend by Month')
plt.ylabel('Spend')
plt.tight_layout()
plt.show()
