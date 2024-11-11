import polars as pl
from sklearn.preprocessing import LabelEncoder
import numpy as np 
from sklearn.metrics.pairwise import cosine_similarity


def encoding(df: pl.DataFrame) -> pl.DataFrame: 
    """ 
    Args:
         : 
         :   
        
    Returns:
        pl.DataFrame:  
    """
    df = df.select(pl.col('fullVisitorId'),pl.col('country'), 
              pl.col('browser'),pl.col('transactionId'),
              pl.col('v2ProductName'))
    
    df = df.with_columns(pl.when(pl.col('transactionId') != 'null').then(1).
                         otherwise(0).alias("transactionId"))
    
    purchases_df = df.filter(pl.col('transactionId') == 1)

    encoder = LabelEncoder()

    for i in purchases_df.columns:
        if i == 'transactionId' or i == 'fullVisitorId':
            continue
        encoder.fit(purchases_df.select(pl.col(f'{i}')))
        encoded_data = encoder.transform(purchases_df.select(pl.col(f'{i}')))
        purchases_df = purchases_df.with_columns(pl.Series(f'{i}', encoded_data))
    
    return purchases_df

def calculate_similarity(user_profiles: pl.DataFrame, user_profiles_no_id: pl.DataFrame, 
                         active_users: pl.DataFrame) -> dict[str,int]:
    """ 
    Args:
        : 
        :   
        
    Returns:
        pl.DataFrame:  
    """
    profile_avg_similarity = {}
    for i in range(0,len(user_profiles)):
        user_profile_df = np.vstack(user_profiles_no_id[i]).T
        avg_similarity = cosine_similarity(user_profile_df, [active_users[-1]])
        avg_similarity = avg_similarity.mean()
        profile_avg_similarity[f'{user_profiles['fullVisitorId'][i]}'] = avg_similarity
    return profile_avg_similarity

def sort_similarities(profile_avg_similarity: dict) -> dict[str,int]:
    """ 
    Args:
        : 
        :   
        
    Returns:
        pl.DataFrame:  
    """
    sorted_dict = sorted(profile_avg_similarity.items(), key=lambda x: x[1])
    return sorted_dict

def recommendation(df: pl.DataFrame, similarity_dict: dict) -> pl.DataFrame: 
    """ 
    Args:
        : 
        :   
        
    Returns:
        pl.DataFrame:  
    """
    recommendations = df.filter((pl.col('fullVisitorId') == similarity_dict[-1][0]) & ((pl.col('transactionId') != "null")))
    recommendations = recommendations.select(pl.col('v2ProductName')).unique()
    return recommendations