import pandas as pd 
from datetime import datetime  

class Transform: 
    def __init__(self):
        self.date = datetime.today().strftime('%Y-%m-%d')

    def data_quality(self, data: dict[str,any]) -> pd.DataFrame:
        df = pd.DataFrame(data)

        df = df[df['product_type'] == 'Honey']

        return df

    def clean_data(self, data: list[any]) -> pd.DataFrame: 

        df = pd.DataFrame(data) 

        df['price_per_oz'] = df['price_per_oz'].str.replace('$', '')
        df['price_per_oz'] = df['price_per_oz'].astype(float)

        df['date_acquired'] = self.date

        return df 
        