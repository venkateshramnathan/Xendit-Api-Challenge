# -*- coding: utf-8 -*-
"""
Created on Mon Sep 24 16:37:55 2018

@author: Venkatesh
"""

#import requests
import pandas as pd
from alpha_vantage.timeseries import TimeSeries
from alpha_vantage.alphavantage import AlphaVantage as av  
from pprint import pprint
import json
import urllib.request
from ta import volatility as vol

#requests.get("https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=PIHPP&apikey=7Y9XI9DTQT3PGWBM&outputsize=compact")

df = pd.read_csv("C:/Users/user/Downloads/companylist.csv")

data = df['Symbol'][1:101]

symbols = data.values.tolist()

ts = TimeSeries(key='7Y9XI9DTQT3PGWBM',output_format='pandas',indexing_type='symbol')
data, metadata = ts.get_daily(symbol='PIHPP',outputsize='compact')
pprint(data.tail(n=2))


QUERY_URL = "https://www.alphavantage.co/query?function={REQUEST_TYPE}&apikey={KEY}&symbol={SYMBOL}&outputsize={OUTPUTSIZE}"
API_KEY = "7Y9XI9DTQT3PGWBM"

stock_values = []

def request(symbol, req_type):
    with urllib.request.urlopen(QUERY_URL.format(REQUEST_TYPE=req_type, KEY = API_KEY, SYMBOL = symbol, OUTPUTSIZE = 'compact')) as req:
        data = req.read().decode("UTF-8")
    return data

def get_daily_data(symbol):
    js = json.loads(request(symbol, "TIME_SERIES_DAILY"))
    #return pandas.DataFrame.from_dict(js["Time Series (Daily)"]["2018-09-27"], orient="index").T
    
    jstring = 'Time Series (Daily)'
    #jstring1 = '2018-09-27'
    for entry in js:
        if entry == jstring:
            i = js[jstring].keys()
            for jkeys in i:
                if jkeys == '2018-09-27':
                    return((jkeys, symbol, 
                            js[jstring][jkeys]['1. open'],
                            js[jstring][jkeys]['2. high'], 
                            js[jstring][jkeys]['3. low'],
                            js[jstring][jkeys]['4. close'],
                            js[jstring][jkeys]['5. volume']))
    return 'api limit'          

        
for items in symbols:
    stock_values.append((get_daily_data(items)))

stock_df = pd.DataFrame(stock_values)

stock_df = stock_df[[1,3,4,5]][0:4]

vol.average_true_range(stock_df[3].astype(float), stock_df[4].astype(float), stock_df[5].astype(float), n=1, fillna=False)


class TimeSeries(av):    
    def get_batch_stock_quotes(self, symbols):
        _FUNCTION_KEY = "BATCH_STOCK_QUOTES"
        return _FUNCTION_KEY, 'Stock Quotes', 'Meta Data'

ts.get_batch_stock_quotes(symbols)