from app.PLAQ.config import mongo_client,db,path_to_save
from app.celery_config import app
import json
import os


@app.task(name="PLAQ - Report Historic")
def generate_report_inventory_active():
    print("Ejecutando PLAQ - Report Historic")

    field_collection = db['field_planting_records'] 
    conf_collection = db['conf_planting_records']

    pipeline_field_historic = [
        {'$unwind': '$RECORD'},
        {'$addFields': {
            'RECORD.FARM': '$FARM',
            'RECORD.BLOCK': '$ID_BLOCK'
        }},
        {'$replaceRoot': {'newRoot': '$RECORD'}}
    ]

    pipeline_conf_historic = [
        {'$unwind': '$RECORD'},
        {'$addFields': {
            'RECORD.FARM': '$FARM',
            'RECORD.BLOCK': '$ID_BLOCK'
        }},
        {'$replaceRoot': {'newRoot': '$RECORD'}},
        {'$unwind': '$TRAYS'},
        {'$replaceRoot': {
            'newRoot': {'$mergeObjects': ['$$ROOT', '$TRAYS']}
        }},
        {'$unset': 'TRAYS'}
    ]

    # Ejecutar la agregación
    approved1 = list(field_collection.aggregate(pipeline_field_historic))
    approved2 = list(conf_collection.aggregate(pipeline_conf_historic))

    # Definir las rutas de los archivos
    field_file_path = f'{path_to_save}/field_planting_hist.json'
    conf_file_path = f'{path_to_save}/conf_planting_hist.json'

    # Eliminar archivos existentes
    try:
        os.remove(field_file_path)
        os.remove(conf_file_path)
    except FileNotFoundError:
        print("Uno o más archivos no se encontraron y no se pudieron eliminar.")

    # Guardar resultados en archivos JSON
    with open(field_file_path, 'w') as fp:
        json.dump(approved1, fp)

    with open(conf_file_path, 'w') as fp:
        json.dump(approved2, fp)

    # Cerrar la conexión
    mongo_client.close()