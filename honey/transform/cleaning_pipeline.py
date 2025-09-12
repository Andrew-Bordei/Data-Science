import pandas as pd 
import numpy as np 

def cleaning_pipeline(df: pd.DataFrame) -> pd.DataFrame: 
    """
    Clean the dataframe  
    """ 
    df = df.fillna(np.nan)

    # Select only 1 upc code per product 
    df['product_upc'] = df['product_upc'].astype(str).str.split().str[0] 

    df['weight'] = df['weight'].str.replace('[A-Za-z#]', '', regex=True)
    
    df['product_rating'] = df['product_rating'].replace({'out of 5 stars': ''}, regex=True)

    df['bought_last_month'] = df['bought_last_month'].replace({r'\+ bought in past month': ''}, regex=True)
    df['bought_last_month'] = df['bought_last_month'].replace({'[Kk]': '000'}, regex=True)

    df['num_reviews'] = df['num_reviews'].str.extract(r'(\d+)')

    df['honey_seller_rank'] = df['honey_seller_rank'].str.extract(r'(\d+)')

    df['food_rank'] = df['food_rank'].str.split('in').str[0]
    df['food_rank'] = df['food_rank'].replace({r'[#A-Za-z:(,)?]': ''}, regex=True)
    df['food_rank'] = df['food_rank'].str.strip()

    # Convert columns to their respective datatypes 
    df['price'] = df['price'].astype(float)
    df['num_reviews'] = df['num_reviews'].astype(float)
    df['product_rating'] = df['product_rating'].astype(float)
    df['bought_last_month'] = df['bought_last_month'].astype(float)
    df['weight'] = df['weight'].astype(float)
    df['honey_seller_rank'] = df['honey_seller_rank'].astype(float)
    df['food_rank'] = df['food_rank'].astype(float)

    df['price_per_ounce'] = round((df['price'] / df['weight']), 2)

    # Nan values changed to comply with MySQL data type constraints 
    df = df.replace({np.nan: None})
    
    return df 