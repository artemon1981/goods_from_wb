import asyncio
import json

import aiohttp
from celery import shared_task
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.core.config import settings
from app.core.db import get_async_session
from app.core.models.product import Product
from app.schemas.product import ProductSchema

app = FastAPI(title=settings.app_title)


async def fetch_product_from_wb(
    nm_id: int, session: AsyncSession = Depends(get_async_session)
):
    """
    Получает данные о продукте с Wildberries по идентификатору nm_id и сохраняет их в базу данных.
    """
    url = f"https://card.wb.ru/cards/v1/detail?appType=1&curr=rub&dest=-2228342&spp=27&nm={nm_id}"

    async with aiohttp.ClientSession() as client_session:
        async with client_session.get(url) as response:
            if response.status != 200:
                raise HTTPException(
                    status_code=response.status, detail="Ошибка получения товара с WB"
                )
            response_text = await response.text()
            data = json.loads(response_text)

            if not data['data']['products']:
                raise HTTPException(
                    status_code=404, detail="Продукт не найден"
                )

            product_info = data["data"]["products"][0]

            product_data = {
                'nm_id': nm_id,
                "current_price": product_info["salePriceU"] / 100,
                "sum_quantity": product_info["totalQuantity"],
                "quantity_by_sizes": [size["origName"] for size in product_info["sizes"]]
            }

    return product_data

async def validate_and_update_product(session: AsyncSession, nm_id: int):
    """
    Проверяет, существует ли продукт с данным nm_id в базе данных. Если продукт не найден,
    данные запрашиваются с Wildberries, и продукт добавляется в базу данных.
    """
    result = await session.execute(select(Product).where(Product.nm_id == nm_id))
    product = result.scalar_one_or_none()

    if not product:
        data = await fetch_product_from_wb(nm_id)
        product = Product(**data)
        session.add(product)
        await session.commit()
        await session.refresh(product)

    return product


@app.get("/product/{nm_id}", response_model=ProductSchema)
async def get_product(nm_id: int, session: AsyncSession = Depends(get_async_session)):
    """
    Эндпоинт для получения продукта по его nm_id. Если продукта нет в базе данных,
    он будет загружен с Wildberries и добавлен в базу.
    """
    product = await validate_and_update_product(session, nm_id)
    if not product:
        raise HTTPException(status_code=404, detail="Товар не найден")
    return product


@shared_task
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
