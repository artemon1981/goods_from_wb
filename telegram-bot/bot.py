import logging
import os

from redis.asyncio import Redis
import httpx
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.fsm.storage.memory import MemoryStorage
from dotenv import load_dotenv
from aiogram import F

load_dotenv()

API_TOKEN = os.getenv("API_TOKEN")
REDIS_URL = os.getenv("REDIS_URL")

logging.basicConfig(level=logging.INFO)

# Настройка бота
bot = Bot(token=API_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)

# Настройка Redis
redis = Redis.from_url(REDIS_URL)


async def rate_limit(user_id: int, limit: int = 60):
    """
    Проверка и установка ограничения частоты запросов.
    """
    if await redis.exists(f"rate_limit:{user_id}"):
        return False
    await redis.set(f"rate_limit:{user_id}", 1, ex=limit)
    return True


async def send_welcome(message: Message):
    """
    Отправка сообщения при использовании команд `/start` или `/help`.
    """
    await message.reply("Привет! Отправь мне ID товара (nm_id), и я расскажу тебе о нём.")


async def product_info_handler(message: Message):
    """Обработка запросов пользователей."""
    try:
        nm_id = message.text.strip()

        if not nm_id.isdigit():
            await message.answer("Пожалуйста, отправьте корректный ID товара.")
            return

        user_id = message.from_user.id

        if not await rate_limit(user_id):
            await message.answer("Слишком много запросов! Подождите минуту.")
            return

        url = f"{os.getenv('API_URL')}{nm_id}"
        print(url)
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
            print(response)

        if response.status_code != 200:
            raise Exception("Товар не найден")
        product_info = response.json()

        nm_id = product_info["nm_id"]
        price = product_info["current_price"]
        sum_quantity = product_info["sum_quantity"]

        details = []
        for size_info in product_info["quantity_by_sizes"]:
            if not isinstance(size_info, str):
                size = size_info["size"]
                details.append(f"Размер: {size}")
                for wh_info in size_info["quantity_by_wh"]:
                    details.append(
                        f"    Склад: {wh_info['wh']}, "
                        f"Остаток: {wh_info['quantity']}"
                    )
                details_str = "\n".join(details)
            else:
                details_str = size_info

        response_message = (
            f"Товар с артикулом: {nm_id}\n"
            f"Текущая цена: {price} руб.\n"
            f"Остаток: {sum_quantity} шт.\n"
            f"Детали по размерам и складам:\n{details_str}"
        )

        await message.answer(response_message, parse_mode="Markdown")
    except Exception as e:
        await message.answer(f"Ошибка: {str(e)}")


# Регистрируем обработчики
dp.message.register(send_welcome, Command(commands=["start", "help"]))
dp.message.register(product_info_handler, F.text)

if __name__ == "__main__":
    dp.run_polling(bot)