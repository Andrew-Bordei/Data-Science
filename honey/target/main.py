from session import Session
from extract import Extract
from transform import Transform
from load import Load
from headers import TARGET_HEADERS

def target_pipeline() -> str:
    # Instantiate all classes (move this somewhere else??)
    session = Session(TARGET_HEADERS)
    extract = Extract()
    transform = Transform()
    load = Load()
    
    # Execute the pipeline 
    data = extract.traverse_all_pages(session)
    df = transform.clean_data(data)
    load_data = load.insert_data(df, "target_honey_data")

    return load_data

if __name__ == '__main__': 
    target_pipeline()
