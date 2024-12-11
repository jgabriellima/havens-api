from api_template.celery.config.celery_settings import celery_settings


class CeleryConfig:
    broker_url = celery_settings.CELERY_BROKER_URL
    result_backend = celery_settings.CELERY_RESULT_BACKEND
    broker_connection_retry = True
    broker_connection_retry_on_startup = True
    broker_connection_max_retries = 10
    broker_connection_timeout = 120
    broker_transport_options = {
        'queue_order_strategy': 'priority',
        'heartbeat': 600,
        'tcp_keepalive': True,
    }

    task_serializer = "json"
    result_serializer = "json"
    accept_content = ["json"]
    timezone = "UTC"
    enable_utc = True

    task_routes = {
        # "api_template.celery.tasks.user_tasks.*": {"queue": "user_tasks"},
        # "api_template.celery.tasks.general_tasks.*": {"queue": "general_tasks"},
    }

    task_default_queue = "default"
    task_queues = {"default": {}, "user_tasks": {}, "general_tasks": {}}

    task_queue_max_priority = 10
    task_default_priority = 5

    worker_prefetch_multiplier = 1
    worker_max_tasks_per_child = 5
    worker_max_memory_per_child = 500000
    worker_concurrency = 4
    worker_cancel_long_running_tasks_on_connection_loss = True

    task_track_started = True
    task_time_limit = 1200
    task_soft_time_limit = 1140
    task_acks_late = True
    task_reject_on_worker_lost = False
    task_acks_on_failure_or_timeout = True

    task_publish_retry = True
    task_publish_retry_policy = {
        'max_retries': 3,
        'interval_start': 1,
        'interval_step': 2,
        'interval_max': 30,
    }

    broker_heartbeat = 600
    broker_heartbeat_checkrate = 2.0
    broker_pool_limit = 20
