import logging

import aiohttp
from aiogram import Bot, Dispatcher, types
from aiogram.fsm.storage.memory import MemoryStorage
from dotenv import load_dotenv

load_dotenv()

API_TOKEN = 'YOUR_TELEGRAM_BOT_TOKEN'
FASTAPI_URL = 'http://fastapi:8000/'

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)

@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await message.reply("Привет пришли мне id товара, я скажу тебе об остатках на складе.")

@dp.message_handler()
async def fetch_product(message: types.Message):
    product_id = message.text.strip()
    if not product_id.isdigit():
        await message.reply("Пришли корректное id.")
        return

    async with aiohttp.ClientSession() as session:
        async with session.get(f"{FASTAPI_URL}{product_id}") as response:
            if response.status == 200:
                product = await response.json()
                product_details = (
                    f"Товар: {product.nm_id}\n"
                    f"Цена: {product.current_price} руб.\n"
                    f"Остатки на складах: {product.sum_quantity}\n"
                    f"Размеры: {product.quantity_by_sizes}"
                )
                await message.reply(product_details)
            else:
                await message.reply("Продукт не найден.")

if __name__ == "__main__":
    dp.run_polling(bot)