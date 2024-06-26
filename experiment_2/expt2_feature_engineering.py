# -*- coding: utf-8 -*-
"""Sushant_Nair_EXPT2.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1ZMO7Fgh2ABQbCgvgJy_uHptE9jPDA0zN
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

#from google.colab import drive
#drive.mount('/content/drive')

data = pd.read_csv('D:/26th_December_2023_Air_Quality_Dataset.csv')

# Create a list of temperature values
temperature_values = ['Hot', 'Moderate', 'Cold']

# Add a new column 'Air Temperature' with alternating "Hot", "Moderate" and "Cold".
data['Air Temperature'] = [temperature_values[i % len(temperature_values)] for i in range(len(data))]

print(data.head())

print(data.info())

data1 = data.copy()

# This step is applied only to those columns which have string data. Columns with numerical data are handled later
columns = ['country','state','city','station','station_code','pollutant_id', ]
for col in columns:
  print(data1[col].unique())

data1['state'].unique()

state_mapping = {}
val = 1
for state in data1['state'].unique():
    # print(state)
    state_mapping[f'{state}'] = val
    val += 1

city_mapping = {}
val = 1
for city in data1['city'].unique():
    # print(city)
    city_mapping[f'{city}'] = val
    val += 1

station_mapping = {}
val = 1
for station in data1['station'].unique():
    # print(station)
    station_mapping[f'{station}'] = val
    val += 1

pollutant_id_mapping = {}
val = 1
for pollutant_id in data1['pollutant_id'].unique():
    # print(pollutant_id)
    pollutant_id_mapping[f'{pollutant_id}'] = val
    val += 1

data1['station_code'] = data1['station_code'].str.strip()
station_code_mapping = {}
val = 1
for station_code in data1['station_code'].unique():
    # print(station_code)
    station_code_mapping[f'{station_code}'] = val
    val += 1

data1['state'].replace(state_mapping, inplace=True)

data1['city'].replace(city_mapping, inplace=True)

data1['station'].replace(station_mapping, inplace=True)

data1['pollutant_id'].replace(pollutant_id_mapping, inplace=True)

data1['station_code'].replace(station_code_mapping, inplace=True)

# Dropping the country column as it has same data for every row.
# Dropping the id column as it is redundant

data1.drop(columns=['country', 'id'], inplace=True)

"""# **One Hot Encoding**"""

print('One Hot Encoding')

encoded_columns = pd.get_dummies(data1['Air Temperature'])

data2 = data1.join(encoded_columns).drop('Air Temperature', axis=1)

print('Air Temperature column is dropped.')
print(data2.head())

# Drop the column Moderate that can be inferred based on the other two columns Cold and Hot

data2.drop(columns=['Moderate'], inplace=True)

print('Drop the column Moderate that can be inferred based on the other two columns Cold and Hot')
print(data2.head())

"""# **Handling Outliers**"""

print('Handling Outliers')

data3 = data2.copy()
data3['pollutant_max_min_avg'] = (data['pollutant_max'] + data['pollutant_min']) / 2
numeric_cols = ['pollutant_min', 'pollutant_max', 'pollutant_avg', 'pollutant_max_min_avg']
for col in numeric_cols:
  plt.figure(figsize = (5, 5))
  data3.boxplot(column=col)

print(data3.shape)

upper_lim = data3['pollutant_max_min_avg'].quantile(.815)
# lower_lim = data3['pollutant_max_min_avg'].quantile(.000001)
# data3 = data3[(data3['pollutant_max_min_avg'] < upper_lim) & (data3['pollutant_max_min_avg'] > lower_lim)]
data3 = data3[(data3['pollutant_max_min_avg'] < upper_lim)]

print(data3.shape)

plt.figure(figsize = (5, 5))
data3.boxplot(column='pollutant_max_min_avg')

print(data3['pollutant_max_min_avg'].describe())

plt.show()

data4 = data3.copy()

"""# **Binning**"""

print('Binning')

labels = ['Low', 'Moderate', 'High', 'Severe']
data4['pollutant_max_min_bin'] = pd.qcut(data4['pollutant_max_min_avg'], q = 4, labels = labels)

print(data4.head())

print('Unique values of Pollutant Max Min Bin column')
print(data4['pollutant_max_min_bin'].unique())

print('Value counts of  Pollutant Max Min Bin column')
print(data4['pollutant_max_min_bin'].value_counts())

"""# **Imputation**"""

print('Imputation')

data5 = data4.copy()

data5['imputation'] = np.random.randint(1, 1000, data5.shape[0])

print('Data5 with new column called Imputation which has random integer values ranging from 1 to 1000.')
print(data5.head())

RANGE = np.arange(20, 80, 1)

print('Replacing Imputation column values with \'Nan\' value for those value falling within RANGE')
print(data5['imputation'].replace(RANGE, np.nan, inplace = True))

print('Head of Data5')
print(data5.head())

print('Value counts of Imputation column')
print(data5['imputation'].value_counts())

print('Sum of null values in Data5')
print(data5.isnull().sum())

data5['imputation'] = data5['imputation'].fillna(data5['imputation'].median())

print('Head of Data5 after filling null values in Imputation column with median of the values in Imputation column (process known as Imputation)')
print(data5.head())

"""# **Normalization**"""

print('Normalization')

data6 = data5.copy()

print('Printing Imputation column of Data6')
print(data6['imputation'][:7])

data6['normalized'] = (data6['imputation'] - data6['imputation'].min()) / (data6['imputation'].max() - data6['imputation'].min())

print('Printing Normalized column of Data6 (process is known as Normalization)')
print(data6['normalized'][:7])

"""# **Standardization**"""

print('Standardization')

data7 = data5.copy()

print('Printing Imputation column of Data7')
data7['imputation'][:7]

data7['standardized'] = (data7['imputation'] - data7['imputation'].mean()) / data7['imputation'].std()

print('Printing standardized column of Data7 (the process is known as Standardization')
print(data7['standardized'][:7])
