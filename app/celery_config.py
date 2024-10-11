from celery import Celery
from celery.schedules import crontab

app = Celery('tasks', broker='redis://redis:6379/0')

app.conf.task_default_retry_delay = 120  # Tiempo de espera por defecto entre reintentos
app.conf.task_max_retries = 2  # Número máximo de reintentos
app.autodiscover_tasks(['app.cuttings','app.PLAQ'])

app.conf.beat_schedule = {
    # cuttings
    'inventario_activo': {
        'task': 'Cuttings - Report Inventory Active',
        'schedule': crontab(hour='6-17',minute='0,30')
    },
    'esquejes_historico': {
        'task' : 'Cuttings - Report Historic',
        'schedule': crontab(hour=3)

    },
    # plaq
    'historico_siembra': {
        'task': 'PLAQ - Report Historic',
        'schedule': crontab(hour=22)
    },
}



app.conf.timezone = 'America/Bogota'

if __name__ == '__main__':
    app.start()
