from functools import wraps
from celery.utils.log import get_task_logger

logger = get_task_logger(__name__)

def task_logging(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        task_id = args[0].request.id if args else 'unknown'
        logger.info(f"Starting task {func.__name__}[{task_id}]")
        try:
            result = func().__call__(*args, **kwargs)
            logger.info(f"Task {func.__name__}[{task_id}] completed successfully")
            return result
        except Exception as e:
            logger.error(f"Task {func.__name__}[{task_id}] failed: {str(e)}")
            raise
    return wrapper
