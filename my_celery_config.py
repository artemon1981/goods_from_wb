from celery import Celery

celery_app = Celery(
    "app", broker="redis://localhost:6379/0", backend="redis://localhost:6379/0"
)

celery_app.conf.beat_schedule = {
    "update-products-every-5-minutes": {
        "task": "app.main.update_all_products",
        "schedule": 300.0,
    },
}

celery_app.conf.timezone = "UTC"
