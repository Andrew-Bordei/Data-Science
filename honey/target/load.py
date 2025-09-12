import mysql.connector
import pandas as pd 
from config import CONFIG

class Load: 
    def __init__(self):
        self.database = mysql.connector.connect(
            host=CONFIG['host'],
            user=CONFIG['user'],
            password=CONFIG['password'],
            database=CONFIG['database']
        )

    def insert_data(self, df: pd.DataFrame, table_name: str) -> str: 
        """Insert cleaned data into a MySQL table""" 
        my_cursor = self.database.cursor()

        # Convert df to tuple & change nan -> None to comply with mysql reqs 
        data = [tuple(None if pd.isna(x) else x for x in row)
            for row in df.itertuples(index=False, name=None)]

        sql_statement = f"""
            INSERT INTO {table_name} 
            (title, brand, price, 
            price_per_oz, rating, num_reviews, 
            product_type, tcin, date_acquired)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s);
        """
        
        my_cursor.executemany(sql_statement, data)
        self.database.commit()

        return print(f'Clean data successfully inserted into {table_name}!')