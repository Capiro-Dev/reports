from app.celery_config import app
from pymongo import MongoClient
from datetime import datetime, timedelta
import json
import os
# Path
mongo_uri = os.getenv('MONGO_URI')
path_to_save = 'app/data/cuttings'

# Db CHAQ
mongo_client = MongoClient(mongo_uri)
db = mongo_client['CHAQ_TEST']
cuttings_collection = db['cuttingsrecords']

@app.task
def generate_report_inventory_active():
    print("entry")
    today = datetime.now()
    limit_date = today - timedelta(days=90)

    # Pipeline de agregación
    pipeline = [
        {
            '$match': { 'recordDate': { '$gt': limit_date } }
        },
        {
            '$set': {
                'recordDate': { '$dateToString': { 'date': '$recordDate', 'format': '%d-%m-%Y %H:%M:%S' } },
                'updatedAt': { '$dateToString': { 'date': '$updatedAt', 'format': '%d-%m-%Y %H:%M:%S' } },
                'createdAt': { '$dateToString': { 'date': '$createdAt', 'format': '%d-%m-%Y %H:%M:%S' } },
                'dateIn': { '$dateToString': { 'date': '$dateIn', 'format': '%d-%m-%Y %H:%M:%S' } },
                'dateOut': { '$dateToString': { 'date': '$dateOut', 'format': '%d-%m-%Y %H:%M:%S' } },
                'shipmentDateOut': { '$dateToString': { 'date': '$shipmentDateOut', 'format': '%d-%m-%Y %H:%M:%S' } }
            }
        }
    ]


    found_records = list(cuttings_collection.aggregate(pipeline))

    with open(f'{path_to_save}/cuttings.json', 'w') as f:
        json.dump(found_records, f)