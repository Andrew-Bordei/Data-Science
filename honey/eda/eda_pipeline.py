import pandas as pd 
import sys 

sys.path.append('./')

from data_processing.database_operations import *

# Define a function to assign buckets
def assign_bin(rank: float):
    # Handle NaN's
    if pd.isna(rank):
        return 'Others'
    
    # Convert to integer for comparison
    rank = int(rank)

    # refactor this 
    if rank <= 5:
        return 'Top 5'
    elif rank <= 15:
        return 'Top 15'
    elif rank <= 25:
        return 'Top 25'
    elif rank <= 50:
        return 'Top 50'
    elif rank <= 100:
        return 'Top 100'
    else:
        return 'Others'

def eda(df: pd.DataFrame, profit_margin: float) -> pd.DataFrame:

    # Only keep rows that mention Raw Honey somewhere in title or description 
    filter_title = (
        df['title'].str.contains(r'\bRaw\b', case=False, regex=True, na=False) & 
        df['title'].str.contains(r'\bHoney\b', case=False, regex=True, na=False)
    )

    filter_desc = (
        df['product_description'].str.contains(r'\bRaw\b', case=False, regex=True, na=False) & 
        df['product_description'].str.contains(r'\bHoney\b', case=False, regex=True, na=False)
    )

    df = df[filter_title | filter_desc]

    # Exclude Manuka honey because of high price due to medicinal prop. 
    df = df[~df['title'].str.contains("[Mm]anuka")]  

    # Rank the data by number of reviews 
    df['review_rank'] = (
        df.groupby('date_acquired')['num_reviews']
        .rank(method='dense', ascending=False)
    )

    # Give each product a rank bucket 
    df['rank'] = df['review_rank'].apply(assign_bin)

    # Group the data based on rank and date 
    grouped_data = (round(df.groupby(
        ['date_acquired','rank'])[
        ['price_per_ounce', 'bought_last_month', 'product_rating', 'num_reviews']
        ].mean(),2)
    )

    df_group = pd.DataFrame(grouped_data)

    # Calculate profit margin 
    df_group['estimated_monthly_profit'] = df_group['bought_last_month'] * profit_margin

    return df_group

def eda_pipeline(profit: float) -> str:
    # Get data from db 
    df = extract_scraped_data("clean_data")

    # Extract insights 
    df_eda = eda(df, profit)
    # print(df_eda)

    df_eda = round(df_eda,2)

    # Save data to a csv for dashboard plotting 
    df_eda.to_csv("./honey_grouped_data.csv")

    return 'EDA pipeline complete'


if __name__ == '__main__':
    eda_pipeline(5.17)