import pandas as pd
from datetime import datetime  


class Transform: 
    def __init__(self):
        self.date =  datetime.today().strftime('%Y-%m-%d')

    def data_quality(self, data: dict[str,any]) -> pd.DataFrame:
        pass

    def cleaning(self, data: dict[str,any]) -> pd.DataFrame:         
        df = pd.DataFrame(data[0])

        df['date_acquired'] = self.date

        return df
