from celery import Celery
from app.core.config import settings

celery_app = Celery(
    "app", broker={settings.CELERY_BROKER_URL}, backend=settings.CELERY_RESULT_BACKEND
)

celery_app.conf.update(broker_connection_retry_on_startup=True)

celery_app.conf.beat_schedule = {
    "update-products-every-5-minutes": {
        "task": "app.tasks.tasks.update_all_products",
        "schedule": 60,
    },
}

celery_app.conf.timezone = "UTC"
celery_app.autodiscover_tasks(["app.api", "app.tasks"])