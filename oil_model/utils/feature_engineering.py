import pandas as pd 

def oil_production_feature(df: pd.DataFrame, countries: list[str]) -> pd.DataFrame:
    """Takes the mean of oil producers and creates new features. Drops individual 
       oil producer columns  
        
    Args:
        df (pd.DataFrame): feature pd.DataFrame  

    Returns:
        pd.DataFrames: dataframe 
    """
    df['world_oil_production'] = df.loc[:,"libya_oil_production":'usa_oil_production'].mean(axis=1)

    for i in countries:
        df.drop([f'{i}_oil_production'], axis=1,inplace=True)
    
    return df