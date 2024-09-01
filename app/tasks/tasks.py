import asyncio
import logging
from sqlalchemy import select

from app.celery import celery_app
from app.core.db import AsyncSessionLocal
from app.core.models.product import Product
from app.main import fetch_product_from_wb


@celery_app.task
def update_all_products():
    """
    Задача Celery для обновления всех продуктов в базе данных.
    Получает все идентификаторы продуктов (nm_id) из базы данных
    и обновляет информацию о каждом продукте с Wildberries.
    """
    logging.info("Обновление базы данных запущено.")

    async def update():
        async with AsyncSessionLocal() as session:
            try:
                # Получаем все nm_ids из базы данных
                result = await session.execute(select(Product.nm_id))
                nm_ids = result.scalars().all()

                # Обрабатываем каждый nm_id
                for nm_id in nm_ids:
                    await fetch_product_from_wb(nm_id, session)
            except Exception as e:
                logging.error(f"Ошибка при обновлении продуктов: {str(e)}")
                raise

    try:
        loop = asyncio.get_event_loop()
        if loop.is_running():
            # Запускаем задачу в существующем цикле
            loop.create_task(update())
        else:
            loop.run_until_complete(update())
    except RuntimeError as e:
        # Обработка случая, когда событийный цикл не запущен
        new_loop = asyncio.new_event_loop()
        asyncio.set_event_loop(new_loop)
        new_loop.run_until_complete(update())

