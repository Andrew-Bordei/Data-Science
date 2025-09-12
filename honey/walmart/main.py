from extract import Extract
from transform import Transform
from load import Load

start_page = 1 
end_page = 26

# Make this a class?? 
def walmart_pipeline(query: str, load_method: str, start_page: int, end_page: int):
    extract = Extract(start_page, end_page, query)
    transform = Transform()
    load = Load()

    data = extract.extraction_process()
    df = transform.cleaning(data)
    load_df = load.controller(load_method, df, 'walmart_honey_data')

    return load_df

if __name__ == '__main__': 
    walmart_pipeline('honey', 'database', start_page, end_page)