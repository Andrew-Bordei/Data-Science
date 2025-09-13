from session import Session
from extract import Extract
from transform import Transform
from load import Load
from headers import TARGET_HEADERS

def target_pipeline(query: str, load_method: str) -> str:
    session = Session(TARGET_HEADERS)
    extract = Extract()
    transform = Transform()
    load = Load()
    
    # Execute the pipeline 
    data = extract.traverse_all_pages(session, query)
    df = transform.clean_data(data)
    load_data = load.controller(load_method, df)

    return load_data

if __name__ == '__main__': 
    target_pipeline('honey', 'database')
