import pandas as pd
import os
import requests
import re
import datetime as dt
import matplotlib.pyplot as plt
import numpy as np
from pandas_datareader import data
import pandas_datareader as web
from bs4 import BeautifulSoup
import json


stocks = ['GOOGL','AAPL','TSLA','AMZN','META', 'SNAP']
User_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36'
curr_dir = os.getcwd()
folder = 'Historical'

# Current Stock prices
base_url = 'https://finance.yahoo.com/quote/'
tickr_url = [f'{x}?p={x}&.tsrc=fin-srch' for x in stocks]

current_price = []
missing_data = []
print('Getting current prices for:')
for tickr,stock in zip(tickr_url,stocks):
    print(f'...{stock}...')
    try:
        content = requests.get(base_url+tickr,headers={'User-Agent':User_agent}).content
        soup = BeautifulSoup(content)
        soup = soup.find('fin-streamer',class_='Fw(b) Fz(36px) Mb(-4px) D(ib)')
        current_price.append(float(soup['value']))
    except:
        print(f'No data for {stock}')
        missing_data.append(stock)
        current_price.append('Na')

df_curr = pd.DataFrame({'Ticker':stocks, 'Current Price':current_price})
try:
    df_curr.to_csv(os.path.join(curr_dir,folder,f'current_prices.csv'))
except:
    print(f'No data for {stock}')


# 20Y Historical Stock Prices
base_url = 'https://query1.finance.yahoo.com/v7/finance/download/{}?' 
params = {'range': '20y',
          'interval': '1d',
          'events':'history'}
print('Getting ({}) historical prices for:'.format(params['range']))
for stock in stocks:
    print(f'...{stock}...')
    try:
        os.mkdir('./Historical/{}/{}'.format(params['range'],stock))
        print('New directory completed')
    except FileExistsError:
        print('A directory already exists, additional data for {} is being saved'.format(stock))
    try:
        response = requests.get(base_url.format(stock), params=params,headers={'User-Agent': User_agent}).content
        soup = BeautifulSoup(response)
        ls = str(soup.find('p')).replace('<p>','').splitlines()
        cols = ls[0]
        data = np.array([x.split(',') for x in ls[1:]])
        pd.DataFrame(data=data,columns=cols.split(',')).to_csv(os.path.join(curr_dir,folder,'{}/{}/historical_price.csv'.format(params['range'],stock)))
    except:
        print(f'No data for {stock}')