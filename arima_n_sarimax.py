# -*- coding: utf-8 -*-
"""ARIMA n Sarimax

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1qE-3CVO3iBGvXk6hYykdabcQ1Vj4SJif
"""

# Commented out IPython magic to ensure Python compatibility.
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
# %matplotlib inline

import io

from google.colab import files

files= files.upload()

df = pd.read_csv(io.BytesIO(files['perrin-freres-monthly-champagne-.csv']))

df.head()

df.tail()

df.columns = ["Month","Sales"]
df.head()

df.drop(106, axis=0, inplace=True)

df.drop(105, axis=0, inplace=True)

df["Month"] = pd.to_datetime(df["Month"])

df.set_index('Month', inplace=True)

df.head()

df.plot()

# Test for stationarity
from statsmodels.tsa.stattools import adfuller

test_result= adfuller(df['Sales'])

def adfuller_test(sales):
  result= adfuller(sales)
  labels=['ADF Test Statistics','p-value','#Lags Used','Number of observations Used']
  for value,label in zip(result,labels):
    print(label+' : '+str(value))
  if result[1] <= 0.05:
    print("Strong evidence against nulll hypothesis, Time series is stationary")
  else:
    print("Weak evidence, Time series is not stationary")

adfuller_test(df["Sales"])

# Differencing
df['Sales first difference']= df['Sales'] - df['Sales'].shift(1)

df.head()

df['Seasonal difference'] = df['Sales']- df['Sales'].shift(12)

df.head()

adfuller_test(df['Seasonal difference'].dropna())

df['Seasonal difference'].plot()

# AR Model
from statsmodels.graphics.tsaplots import plot_acf,plot_pacf

fig= plt.figure(figsize=(12,8))
ax1= fig.add_subplot(211)
fig= plot_pacf(df['Seasonal difference'].iloc[13:],lags=40,ax=ax1)
ax2= fig.add_subplot(212)
fig= plot_acf(df['Seasonal difference'].iloc[13:],lags=40,ax=ax2)

from statsmodels.tsa.arima_model import ARIMA

model= ARIMA(df['Sales'], order=(1,1,1))
model_fit=model.fit()

model_fit.summary()

df['forecast']= model_fit.predict(start=90, end=103, dynamic=True)
df[['Sales','forecast']].plot(figsize=(12,8))

import statsmodels.api as sm

model=sm.tsa.statespace.SARIMAX(df['Sales'], order=(1,1,1), seasonal_order=(1,1,1,12))
results= model.fit()

df['forecast']= results.predict(start=90, end=103, dynamic=True)
df[['Sales','forecast']].plot(figsize=(12,8))

