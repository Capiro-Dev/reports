""
from datetime import datetime, timedelta
from app.cuttings.config import mongo_client,db,path_to_save
from app.celery_config import app
import json


@app.task(name="Cuttings - Report Inventory Active")
def generate_report_inventory_active():
    cuttings_collection = db['cuttingsrecords']

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
