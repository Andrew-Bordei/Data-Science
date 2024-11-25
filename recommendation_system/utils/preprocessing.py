import polars as pl
from sklearn.preprocessing import LabelEncoder
import numpy as np 
from sklearn.metrics.pairwise import cosine_similarity


def label_encoding(df: pl.DataFrame) -> pl.DataFrame: 
    """ 
    Args:
         : 
         :   
        
    Returns:
        pl.DataFrame:  
    """
    df = df.select(pl.col('fullVisitorId'),pl.col('country'), pl.col('city'), 
              pl.col('browser'),pl.col('operatingSystem'),pl.col('deviceCategory'),
              pl.col('source'),pl.col('transactionId'),pl.col('v2ProductName'))
    
    df = df.with_columns(pl.when(pl.col('transactionId') != 'null').then(1).
                         otherwise(0).alias("transactionId"))
    
    purchases_df = df

    encoder = LabelEncoder()

    for i in purchases_df.columns:
        if i == 'transactionId' or i == 'fullVisitorId':
            continue
        encoder.fit(purchases_df.select(pl.col(f'{i}')))
        encoded_data = encoder.transform(purchases_df.select(pl.col(f'{i}')))
        purchases_df = purchases_df.with_columns(pl.Series(f'{i}', encoded_data))
    
    return purchases_df

def target_encoding(df: pl.DataFrame) -> pl.DataFrame:
    """ 
    Args:
         : 
         :   
        
    Returns:
        pl.DataFrame:  
    """
    df = df.select(pl.col('fullVisitorId'),pl.col('country'), pl.col('city'), 
              pl.col('browser'),pl.col('operatingSystem'),pl.col('deviceCategory'),
              pl.col('source'),pl.col('transactionId'),pl.col('v2ProductCategory'))
    
    df = df.with_columns(pl.when(pl.col('transactionId') != 'null').then(1).
                         otherwise(0).alias("transactionId"))
    
    for i in df.columns:
        if i == 'date' or i == 'visitStartTime' or i == 'fullVisitorId' or i == 'transactionId':
            continue 
        category_means = df.group_by(pl.col(f'{i}')).agg(
            pl.col('transactionId').mean()
        )
        df = df.join(category_means, on=f'{i}', how='left')
        df = df.with_columns(pl.col("transactionId_right").alias(f"{i}")).drop("transactionId_right")

    return df

def calculate_similarity(user_profiles: pl.DataFrame, user_profiles_no_id: pl.DataFrame, 
                         active_user: np.array) -> dict[str,int]:
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
        avg_similarity = cosine_similarity(user_profile_df, [active_user])
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
    index = -1
    recs = [] 
    
    while len(recs) < 5:
        recommendations = df.filter((pl.col('fullVisitorId') == similarity_dict[index][0]) & ((pl.col('transactionId') != "null")))
        if len(recommendations) > 0:
            recommendations = recommendations.select(pl.col('v2ProductCategory')).unique().item(0,'v2ProductCategory')
            recs.append(recommendations)
        index -= 1

    return recs

def precision(bought: pl.DataFrame, predicted: pl.DataFrame, k: int) -> dict:
    """Evaluates recommendations using precision@k
    
    Args:
        
    
    Returns:

    """
    bought_set = set(bought)
    pred_set = set(predicted[:k])
    result = round(len(bought_set & pred_set) / float(len(pred_set)), 2)

    return result

def recommendation_pipeline(active_user: str, user_profiles: pl.DataFrame, 
                            encoded_df: pl.DataFrame, original_df: pl.DataFrame) -> list[str]:
    """
    
    Args:
        
    
    Returns:

    """
    user_profiles = user_profiles.with_columns(pl.col("fullVisitorId").cast(str))
    encoded_df = encoded_df.with_columns(pl.col("fullVisitorId").cast(str))

    user_profiles = user_profiles.filter(pl.col("fullVisitorId") != f"{active_user}")

    user_profiles_no_id = user_profiles.drop("fullVisitorId")
    user_profiles_no_id = user_profiles_no_id.to_numpy()

    active_user_data = list(encoded_df.filter(pl.col("fullVisitorId") == f"{active_user}").row(-1))[1:]
    similarities = calculate_similarity(user_profiles, user_profiles_no_id, active_user_data)
    sorted_dict = sorted(similarities.items(), key=lambda x: x[1])
    rec = recommendation(original_df,sorted_dict)

    return rec

def recommendation_eval_pipeline(active_user: str, user_profiles: pl.DataFrame, 
                                 encoded_df: pl.DataFrame, original_df: pl.DataFrame) -> float:
    """
    
    Args:
        
    
    Returns:

    """
    actual_bought = original_df.filter((pl.col('fullVisitorId') == f"{active_user}") & (pl.col('transactionId') != 'null')
                                       ).select(pl.col('v2ProductCategory')).to_series().to_list()
    rec_precision = precision(actual_bought, 
                              recommendation_pipeline(active_user, user_profiles, 
                                                      encoded_df, original_df),5)
    
    return rec_precision

def user_profiles(encoded_df: pl.DataFrame) -> pl.DataFrame:
    user_profiles = encoded_df.group_by(pl.col('fullVisitorId')).agg(
        pl.col('country'), pl.col('city'), 
        pl.col('browser'),pl.col('operatingSystem'),pl.col('deviceCategory'),
        pl.col('source'),pl.col('transactionId'),pl.col('v2ProductCategory')
    )
    user_profiles = user_profiles.with_columns(pl.col("fullVisitorId").cast(str))
    return user_profiles