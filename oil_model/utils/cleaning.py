import pandas as pd 
from fredapi import Fred
import yfinance as yf 
from functools import reduce
from datetime import datetime

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

def merge_df(df_list: list[pd.DataFrame]) -> pd.DataFrame:
    """Will return a dataframe that has been merged from list of dataframes  
        
    Args:
        df (list): List of pd.DataFrames that have been cleaned 

    Returns:
        pd.DataFrames: merged dataframe 
    """
    merged_df = reduce(lambda left,right: pd.merge(left,right,on=['Date'], how='outer'),df_list)

    return merged_df

def get_oil_data(dict: dict()) -> pd.DataFrame:
    """Downloads oil production data from FRED API, saves each df to a list 
        
    Args:
        dict dict(): Dictionary with countries and dataset key     
    Returns:
        pd.DataFrame: List of dataframes with oil production data  
    """
    dataframes = []
    for key in dict: 
        df = pd.DataFrame({f"{key}_oil_production":fred.get_series(f'{dict[key]}')})
        dataframes.append(df)

    return dataframes

def get_financial_data(dict: dict(), start: datetime, end: datetime) -> pd.DataFrame: 
    """Doanloads financial data frome Yahoo Finance API, saves each df to a list 
        
    Args:
        dict dict(), start datetime, end datetime: Dictionary with dataset keys to download, start & end date  
    Returns:
        pd.DataFrame: List of dataframes with financial data  
    """
    dataframes = []
    for key in dict: 
        df = pd.DataFrame({f"{key}":yf.download(f"{dict[key]}", start=start, end=end)['Adj Close']})
        dataframes.append(df)

    return dataframes

def axis_manipulation(df: pd.DataFrame) -> pd.DataFrame:
    """Renaming axis to be consistent  
        
    Args:
        df pd.DataFrame: dataframe  
    Returns:
        pd.DataFrame: dataframe  
    """
    for i in df:
        i.rename_axis(index="Date",inplace=True)
    
    return df

def resample_data(df: pd.DataFrame) -> pd.DataFrame:
    """Changes the data sampling from monthly, yearly to daily. Filling the nan values with respective row entry  
        
    Args:
        df pd.DataFrame: dataframe 
    Returns:
        pd.DataFrame: dataframe 
    """
    for i in range(len(df)):
        df[i] = df[i].resample('D').ffill()
    
    return df


