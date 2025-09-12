from extract import Extract
from transform import Transform
from load import Load

start_page = 1 
end_page = 26
query = 'honey'

def walmart_pipeline():
    extract = Extract(start_page, end_page, query)
    transform = Transform()
    load = Load()

    data = extract.extraction_process()
    df = transform.cleaning(data)
    load_df = load.insert_data(df, 'walmart_honey_data')

    return load_df

if __name__ == '__main__': 
    walmart_pipeline()