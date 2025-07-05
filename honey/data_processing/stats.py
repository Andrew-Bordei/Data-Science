import pandas as pd 
import plotly.express as px

def descriptive_stats(df: pd.DataFrame, profit_margin: float) -> dict[str:float]:
    """
    Calculate and return statistics of the data 
    """
    avg_price = round(df['price'].mean(), 2)

    avg_price_per_ounce = round(df['price_per_ounce'].mean(), 2)

    price_per_ounce_stdev = round(df['price_per_ounce'].std(), 2)

    avg_rating = round(df['product_rating'].mean(), 2)

    avg_bought = round(df['bought_last_month'].mean(), 2)

    stdev_bought = round(df['bought_last_month'].std(), 2)

    avg_reviews = round(df['num_reviews'].mean(), 2)

    # Estimated monthly profit 
    monthly_profit = round(df['bought_last_month'].mean() * profit_margin, 2)

    # Estimated yearly profit 
    yearly_profit = round(monthly_profit * 12, 2)

    stats = {
        "average price":avg_price, "average price per ounce": avg_price_per_ounce, 
        "price_per_ounce_stdev": price_per_ounce_stdev, 
        "average product rating":avg_rating, "average number of reviews": avg_reviews,
        "average bought last month":avg_bought,"standard dev bought last month": stdev_bought, 
        "Estimated monthly profit": monthly_profit, "Estimated yearly profit":yearly_profit
    }

    return stats

class VisualizeData:
    """
    Class to plot stratified samples from the data 
    """
    def __init__(
        self, df: pd.DataFrame, 
        key: str, 
        title: str, 
        x: str, 
        y: str, 
        graph_type: str,
    ):
        self.df = df
        self.key = key 
        self.title = title 
        self.x = x 
        self.y = y 
        self.graph_type = graph_type

    def compute_stats(self, df: pd.DataFrame) -> list[dict[str, float]]:
        top5 = descriptive_stats(df[:5])
        top10 = descriptive_stats(df[6:15])
        top25 = descriptive_stats(df[16:25])
        top50 = descriptive_stats(df[25:50])
        top100 = descriptive_stats(df[51:100])

        return [top5, top10, top25, top50, top100]
    
    def get_data(self, stats: list[dict[str: float]]) -> list[dict[str], dict[float]]:
        data = {
            'Top 5': stats[0].get(f'{self.key}'), 
            'Top 15': stats[1].get(f'{self.key}'),
            'Top 25': stats[2].get(f'{self.key}'), 
            'Top 50': stats[3].get(f'{self.key}'), 
            'Top 100': stats[4].get(f'{self.key}'),
        }

        return data

    def display(self, x: dict[str], y: dict[float], graph_type: str) -> px: 
        if graph_type == 'bar':
            fig = px.bar(
                x=x, y=y, 
                title=f'{self.title}', 
                labels={'x':f'{self.x}','y':f'{self.y}'},
                width=700, 
                height=700
            )
        elif graph_type == 'line':
            fig = px.line(
                x=x, y=y, 
                title=f'{self.title}', 
                labels={'x':f'{self.x}','y':f'{self.y}'},
                height=700, width=700,
            ) 

        return fig.show()
    
    def main(self):
        """
        Function to automate creation & visualization of data 
        """
        stats = self.compute_stats(self.df)

        data = self.get_data(stats)

        self.display(
            data.keys(), 
            data.values(), 
            self.graph_type, 
        )
 