import pandas as pd 
import matplotlib.pylab as plt
import seaborn as sns 

def kde(data_df: pd.DataFrame, x_value: pd.Series) -> plt.Figure:
    """ Plots a kernal density estimate of a given dataframe 
        
    Args:
        df (pd.DataFrame), x (pd.Series): Dataframe and a column to plot 
        

    Returns:
        plt.Figure: Plotted data 
    """
    sns.kdeplot(data=data_df, x=x_value)
    plt.show()

def heat_map(data_df: pd.DataFrame) -> plt.Figure:
    """ Returns a heat map figure with the correlations from a dataframe 
        
    Args:
        df (pd.DataFrame): Dataframe 

    Returns:
        plt.Figure: Correlation map  
    """
    # Printing heat map with correlations
    plt.figure(figsize=(13,5))
    sns.heatmap(round(data_df.corr(),2),annot=True, cmap='Blues')
    plt.show()