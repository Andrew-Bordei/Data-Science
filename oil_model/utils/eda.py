import pandas as pd 
import matplotlib.pylab as plt
import seaborn as sns 

def kde(data_df,x_value):
    sns.kdeplot(data=data_df, x=x_value)
    plt.show()

def heat_map(data_df):
    # Printing heat map with correlations
    plt.figure(figsize=(13,5))
    sns.heatmap(round(data_df.corr(),2),annot=True, cmap='Blues')
    plt.show()