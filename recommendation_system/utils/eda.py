import seaborn as sns
import matplotlib.pyplot as plt
import polars as pl

def print_popular_stats(df: pl.DataFrame, category: str) -> pl.DataFrame:
    """Returns a df with most for most popular stats based on category 
    Args:
        str: Column name
        pl.DataFrame: df 
        
    Returns:
        pl.DataFrame: df 
    """

    # print(f"10 most popular {category}:")
    return df.select(pl.col(f"{category}").value_counts(sort=True)).unnest(f'{category}')[:10]

def list_comprehension(array: list[int], input_type: str) -> list[int]:
    """Returns a list comprehension for either item id's or frequency of purchases 
    Args:
        array list[int] : Integer array, corresponds to either key, value of dict 
        inpute_type(str) : Determines whether to loop through keys or values   
        
    Returns:
        list[int]: array of integers 
    """
    match input_type:
        case "items":
            return [x for x,i in array]
        case "frequency":
            return [i for x,i in array]
        case _:
            return "Not valid. Please check the params"
        
def bar_plot(x: list[int], y: list[int], title: str) -> plt.Figure:
    """ Plots a bar chart 
    Args:
        x list[int] : List of integers of X values to be plotted  
        y list[int] : List of integers of Y values to be plotted
        title (str) : The respective title of the graph 
        
    Returns:
        plt.Figure: Bar plot of the provided data 
    """
    fig, ax = plt.subplots(figsize=(12,8))
    plt.title(title)
    sns.barplot(x=x, y=y, ax=ax, color="#1c4ede")
    plt.xticks(rotation=90)
    plt.show()

def pie_chart(data: pl.Series, labels: list[str], title: str) -> plt.Figure:
    """ Plots a pie chart with provided data 
    Args:
        data list[int] : Series of integers  
        labels list[int] : Respective labels for each integer
        title (str) : The respective title of the graph 
        
    Returns:
        plt.Figure: Pie chart of the provided data 
    """
    
    plt.subplots(figsize=(12, 8))
    plt.pie(data,labels=labels,autopct='%.1f%%',labeldistance=1.1,
            shadow=True,startangle=60)
    plt.title(title)
    plt.show()