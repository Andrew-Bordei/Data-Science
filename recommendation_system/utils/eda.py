def list_comprehension(array_items: list[int]) -> plt.Figure:
    """  
        
    Args:
        df (pd.DataFrame), x (pd.Series): Dataframe and a column to plot 
        

    Returns:
        plt.Figure: Plotted data 
    """
    sns.kdeplot(data=data_df, x=x_value)
    plt.show()