import asyncio
import logging
from sqlalchemy import select

from app.celery import celery_app
from app.core.db import get_async_session
from app.core.models.product import Product
from app.main import fetch_product_from_wb


@celery_app.task
def update_all_products():
    """
    Задача Celery для обновления всех продуктов в базе данных. Получает все идентификаторы продуктов (nm_id)
    из базы данных и обновляет информацию о каждом продукте с Wildberries.
    """
    logging.info("Обновление базы данных запущено.")
    async def update():
        async with get_async_session() as session:
            result = await session.execute(select(Product.nm_id))
            nm_ids = result.scalars().all()

            for nm_id in nm_ids:
                await fetch_product_from_wb(nm_id, session)

    asyncio.run(update())