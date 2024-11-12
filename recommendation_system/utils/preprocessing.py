import polars as pl
from sklearn.preprocessing import LabelEncoder
import numpy as np 
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.metrics import precision_score


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
    index = -1
    recs = [] 
    
    while len(recs) < 3:
        recommendations = df.filter((pl.col('fullVisitorId') == similarity_dict[index][0]) & ((pl.col('transactionId') != "null")))
        print(recommendations)
        recommendations = recommendations.select(pl.col('v2ProductName')).unique()
        recs.append(recommendations)
        index -= 1

    # recommendations = df.filter((pl.col('fullVisitorId') == similarity_dict[-1][0]) & ((pl.col('transactionId') != "null")))
    # recommendations = recommendations.select(pl.col('v2ProductName')).unique()
    return 0

def evaluate_recommendations(df: pl.DataFrame, test_df: pl.DataFrame, similarity_dict: dict, k: int) -> dict:
    """
    Evaluates recommendations using precision.
    
    Args:
        df (pl.DataFrame): Original data containing product interactions.
        test_df (pl.DataFrame): Test data to validate recommendations.
        similarity_dict (dict): Dictionary of user similarities for recommendations.
        k (int): The number of top recommendations to consider.
    
    Returns:
        dict: A dictionary containing precision@k and recall@k.
    """
    # Store evaluation results
    precision_list = []

    for user_id, _ in similarity_dict.items():
        # Generate recommendations for the user
        recommendations = recommendation(df, similarity_dict).head(k)

        # Get ground truth products from the test set
        actual_products = test_df.filter((pl.col('fullVisitorId') == user_id) & (pl.col('transactionId') == 1)).select(pl.col('v2ProductName')).to_list()

        # Calculate Precision@K and Recall@K
        if actual_products:
            relevant_recs = [1 if rec in actual_products else 0 for rec in recommendations['v2ProductName']]
            precision = sum(relevant_recs) / k
            
            precision_list.append(precision)

    # Average the precision and recall across users
    avg_precision = np.mean(precision_list)

    return {'precision@k': avg_precision}