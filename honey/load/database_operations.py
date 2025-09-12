import mysql.connector
import pandas as pd 

def insert_scraped_data(data: list[dict[str:any]], table_name: str, current_date: str) -> str: 
    """
    Insert scraped data into a MySQL table 
    """
    database = mysql.connector.connect(
        host="localhost",
        user="root",
        password="!?65DataToTradr&/93",
        database="honey_data"
    )

    my_cursor = database.cursor()

    for i in data:
        my_cursor.execute(f"INSERT INTO {table_name} (title, brand, weight, price, product_rating,"
        "bought_last_month, num_reviews, product_description, product_upc, date_acquired)" 
        "VALUES (%s, %s, %s, %s, %s, %s, %s, %s , %s, %s);", (
            i["title"], i["brand"], i["weight"],
            i["price"], i["product_rating"], i["bought_last_month"],
            i["num_reviews"], i["description"],
            i["product_upc"], f"{current_date}")
        )
        database.commit()

    my_cursor.close()

    return "Data was successfully inserted into the table"

def extract_scraped_data(table_name: str) -> pd.DataFrame:
    """
    Extract scraped data from a MySQL table 
    """
    database = mysql.connector.connect(
        host="localhost",
        user="root",
        password="!?65DataToTradr&/93",
        database="honey_data"
    )

    my_cursor = database.cursor()

    my_cursor.execute(f"SELECT * FROM {table_name}")

    raw_data = []

    for data in my_cursor:
        raw_data.append(data)
        
    database.close()
    my_cursor.close()

    df = pd.DataFrame(
        raw_data,
        columns = ["index","title", "brand", "weight",'price','price_per_ounce','product_rating',
            'bought_last_month','num_reviews','product_description','product_upc', "date_acquired"])
    
    return df

def insert_clean_data(df: pd.DataFrame, table_name: str) -> int:  
    """
    Insert cleaned data into a MySQL table 
    """ 
    database = mysql.connector.connect(
        host="localhost", 
        user="root",
        password="!?65DataToTradr&/93", 
        database="honey_data"
    )

    # Interface to communicate with database 
    my_cursor = database.cursor()
    
    df = df.drop(columns=['index'], errors='ignore')

    # Convert dataframe to a tuple to comply with executemany requirements 
    data = [tuple(x) for x in df.to_numpy()]

    sql_statement = (f"INSERT INTO {table_name} " 
    "(title, brand, weight, price, price_per_ounce, product_rating, bought_last_month, "
    "num_reviews, product_description, product_upc, date_acquired)"
    "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);")

    my_cursor.executemany(sql_statement, data)

    database.commit()
    my_cursor.close()
    database.close()

    return 'Clean data was successfully inserted!'


