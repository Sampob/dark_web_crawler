from app.config import Config

from celery.schedules import crontab
from celery import Celery

def make_celery() -> Celery:
    """
    Create celery instance.

    :param app: Flask application instance

    :return: Created celery
    """
    celery = Celery(
        "darknet_crawler",
        broker=Config.CELERY_BROKER_URL,
        backend=Config.result_backend,
        CELERY_WORKER_MAX_TASKS_PER_CHILD=1,
    )

    celery.autodiscover_tasks(["app.tasks"])

    parsed_crontabs = Config.CRONTAB

    celery.conf.update(
        worker_hijack_root_logger=False,
        timezone=Config.TIMEZONE,
        beat_schedule={
            "schedule-dynamic-crawls": {
                "task": "app.tasks.schedule_crawls",
                "schedule": crontab(minute=parsed_crontabs[0],
                                    hour=parsed_crontabs[1],
                                    day_of_week=parsed_crontabs[2],
                                    day_of_month=parsed_crontabs[3],
                                    month_of_year=parsed_crontabs[4]
                            ),
            },
        }
    )
    
    celery.conf.broker_connection_retry_on_startup = True

    return celery

celery = make_celery()