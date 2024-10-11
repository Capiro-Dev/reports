from pymongo import MongoClient
import os

mongo_uri = os.getenv('MONGO_URI_CHAQ')
path_to_save = '/app/data/cuttings'
mongo_client = MongoClient(mongo_uri, connect=False)
db = mongo_client['CHAQ']
