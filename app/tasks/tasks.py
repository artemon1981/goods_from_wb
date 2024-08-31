import asyncio

from app.api.background_tasks import save_or_update_product
from app.api.utils import get_product_info
from app.celery import celery_app
from app.core.config import settings
from app.core.db import AsyncSessionLocal, get_async_session
from app.crud.product import product_crud

from app.core.models.product import Product
from app.main import fetch_product_from_wb


@celery_app.task
def update_all_products():
    """
    Задача Celery для обновления всех продуктов в базе данных. Получает все идентификаторы продуктов (nm_id)
    из базы данных и обновляет информацию о каждом продукте с Wildberries.
    """

    async def update():
        async with get_async_session() as session:
            result = await session.execute(select(Product.nm_id))
            nm_ids = result.scalars().all()

            for nm_id in nm_ids:
                await fetch_product_from_wb(nm_id, session)

    asyncio.run(update())