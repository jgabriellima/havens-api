from celery import Celery
from api_template.celery.config.celery_config import CeleryConfig

def get_celery_app():
    app = Celery("api_template")
    app.config_from_object(CeleryConfig())
    app.conf.update(
        worker_send_task_events=True,
        task_send_sent_event=True
    )
    
    # Descoberta automática de tasks
    app.autodiscover_tasks(['api_template.celery.tasks'], force=True)
    
    # Log das tasks registradas
    registered_tasks = app.tasks.keys()
    print("=" * 50)
    print("Registered tasks:")
    for task in registered_tasks:
        print(f"- {task}")
    print("=" * 50)
    
    return app

celery_app = get_celery_app()
