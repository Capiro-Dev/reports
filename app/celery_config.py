from celery import Celery
from celery.schedules import crontab

app = Celery('tasks', broker='redis://redis:6379/0')

app.conf.task_default_retry_delay = 120  # Tiempo de espera por defecto entre reintentos
app.conf.task_max_retries = 2  # Número máximo de reintentos

@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    print("Registered tasks:", sender.tasks.keys())

# cuttings
app.conf.beat_schedule = {
    'inventario_activo': {
        'task': 'app.tasks_cuttings.generate_report_inventory_active',
        'schedule': crontab(hour=9, minute=23),  # cada 60 segundos
    },
    # 'generate_report_2': {
    #     'task': 'app.tasks.generate_report_2',
    #     'schedule': 120.0,  # cada 120 segundos
    # },
}

app.conf.timezone = 'America/Bogota'

if __name__ == '__main__':
    app.start()