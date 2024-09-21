import pandas as pd 
from fredapi import Fred
import yfinance as yf 
from functools import reduce

fred_key = '3932ed65675a268ca1a4e0e68b10fa9b'
fred = Fred(api_key=fred_key)

oil_api_keys = {
    "libya":"LBYNGDPMOMBD",
    "kazak":"KAZNGDPMOMBD",
    "qatar":"QATNGDPMOMBD",
    "iran":"IRNNGDPMOMBD",
    "kuwait":"KWTNGDPMOMBD",
    "uae":"ARENGDPMOMBD",
    "saudi":"SAUNGDPMOMBD",
    "iraq":"IRQNGDPMOMBD"
}

financial_api_keys = {
    "crude_price":"CL=F",
    "sp_500":"ES=F",
    "vix":"^VIX",
    "usd":"DX=F",
}

def merge_df(df):
    merged_df = reduce(lambda left,right: pd.merge(left,right,on=['Date'], how='outer'),df)

    return merged_df

def get_oil_data(key):
    dataframes = []
    for i in key: 
        df = pd.DataFrame({f"{i}_oil_production":fred.get_series(f'{key[i]}')})
        dataframes.append(df)

    return dataframes

def get_financial_data(key,start,end):
    dataframes = []
    for i in key: 
        df = pd.DataFrame({f"{i}":yf.download(f"{key[i]}", start=start, end=end)['Adj Close']})
        dataframes.append(df)

    return dataframes

def axis_manipulation(df):
    for i in df:
        i.rename_axis(index="Date",inplace=True)
    
    return df

def resample_data(df):
    for i in range(len(df)):
        df[i] = df[i].resample('D').ffill()
    
    return df


