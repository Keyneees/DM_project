import os
import pandas as pd
from pymongo import MongoClient

def load_csv_to_mongo(csv_folder, mongo_uri, db_name, collection_name):
    client = MongoClient(mongo_uri)
    db = client[db_name]
    collection = db[collection_name]

    for filename in os.listdir(csv_folder):
        if filename.endswith('.csv'):
            file_path = os.path.join(csv_folder, filename)
            data = pd.read_csv(file_path)
            collection.insert_many(data.to_dict('records'))
            print(f'Loaded {filename} into MongoDB collection {collection_name}.')

if __name__ == '__main__':
    csv_folder = '../dataset/archive'
    mongo_uri = 'mongodb://localhost:27017/'
    db_name = 'local'
    collection_name = 'Formula1'
    
    load_csv_to_mongo(csv_folder, mongo_uri, db_name, collection_name)