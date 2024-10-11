from app.cuttings.config import mongo_client,db,path_to_save
from app.celery_config import app
import json


@app.task(name="Cuttings - Historic")
def generate_report_hiscoric():
    cuttings_collection = db['cuttingsrecords']

    # Pipeline de agregación
    pipeline = [
        {
            '$set': {
                'recordDate': {
                    '$dateToString': {
                        'date': '$recordDate',
                        'format': '%d-%m-%Y %H:%M:%S'
                    }
                },
                'updatedAt': {
                    '$dateToString': {
                        'date': '$updatedAt',
                        'format': '%d-%m-%Y %H:%M:%S'
                    }
                },
                'createdAt': {
                    '$dateToString': {
                        'date': '$createdAt',
                        'format': '%d-%m-%Y %H:%M:%S'
                    }
                },
                'dateIn': {
                    '$dateToString': {
                        'date': '$dateIn',
                        'format': '%d-%m-%Y %H:%M:%S'
                    }
                },
                'dateOut': {
                    '$dateToString': {
                        'date': '$dateOut',
                        'format': '%d-%m-%Y %H:%M:%S'
                    }
                },
                'shipmentDateOut': {
                    '$dateToString': {
                        'date': '$shipmentDateOut',
                        'format': '%d-%m-%Y %H:%M:%S'
                    }
                }
            }
        }
    ]



    found_records = list(cuttings_collection.aggregate(pipeline))

    with open(f'{path_to_save}/cuttings_historic.json', 'w') as f:
        json.dump(found_records, f)
