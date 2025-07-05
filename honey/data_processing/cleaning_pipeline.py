import pandas as pd 
import numpy as np 

def cleaning_pipeline(df: pd.DataFrame) -> pd.DataFrame: 
    """
    Clean the dataframe  
    """ 
    # Replace None with nan values 
    df = df.fillna(np.nan)

    # Select only 1 upc code per product 
    df['product_upc'] = df['product_upc'].astype(str).str.split().str[0] 

    # Strip unnecessary words
    df['weight'] = df['weight'].str.replace('[A-Za-z]', '',regex=True)
    
    # # Strip unnecessary words
    df['product_rating'] = df['product_rating'].replace({'out of 5 stars': ''}, regex=True)

    # Strip unnecessary words 
    df['bought_last_month'] = df['bought_last_month'].replace({r'\+ bought in past month': ''}, regex=True)
    # Make thousands be in numeric format 
    df['bought_last_month'] = df['bought_last_month'].replace({'[Kk]': '000'}, regex=True)

    # Strip the word review  
    df['num_reviews'] = df['num_reviews'].replace({'[Rr]eviews|Review': ''}, regex=True)
    # Eliminate the comma 
    df['num_reviews'] = df['num_reviews'].replace({',': ''}, regex=True)

    # Convert columns to their respective datatypes 
    df['price'] = df['price'].astype(float)
    df['num_reviews'] = df['num_reviews'].astype(float)
    df['product_rating'] = df['product_rating'].astype(float)
    df['bought_last_month'] = df['bought_last_month'].astype(float)
    df['weight'] = df['weight'].astype(float)

    # Calculate price per ounce of each product 
    df['price_per_ounce'] = round((df['price'] / df['weight']), 2)

    # Nan values changed to comply with MySQL data types constraints 
    df = df.replace({np.nan: None})
    
    return df 