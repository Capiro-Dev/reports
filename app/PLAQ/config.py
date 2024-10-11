from pymongo import MongoClient
import os

mongo_uri = os.getenv('MONGO_URI_PLAQ')
path_to_save = '/app/data/PLAQ'
mongo_client = MongoClient(mongo_uri, connect=False)
db = mongo_client['PLAQ']