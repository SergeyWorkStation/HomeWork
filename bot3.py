import datetime
import logging
import os
import asyncio
from aiogram import Bot, Dispatcher, types, BaseMiddleware
from aiogram.types import LabeledPrice, PreCheckoutQuery
from aiogram.filters import Command

BOT_TOKEN = os.environ["TOKEN"]
PROVIDER_TOKEN = os.environ["PROVIDER_TOKEN"]

# Настройка логирования
logging.basicConfig(level=logging.INFO)


# Инициализация бота и диспетчера
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

user_activity = {}


# Список товаров
PRODUCTS = [
    {"title": "Термоноски", "photo": "https://ir-5.ozone.ru/s3/multimedia-1-2/wc1000/7165396694.jpg", "description": "Погрузитесь в зимнюю сказку с теплыми зимними термоносками ALASKA — лучшим решением для холодной погоды! Эти носки созданы для тех, кто ценит комфорт даже в самые сильные морозы. Они мягкие и уютные, а свободная резинка на голени бережно поддерживает ногу, не вызвав дискомфорта.", "price": 730},
    {"title": "Носки THOMASBS", "photo": "https://ir-5.ozone.ru/s3/multimedia-1-n/wc1000/7070257067.jpg", "description": "Представляем вам идеальное решение для любого гардероба – комплект из 12 пар мужских коротких носков THOMAS.", "price": 595},
    {"title": "Пуховик FEROD&NORDE Зима", "photo": "https://ir-5.ozone.ru/s3/multimedia-1-q/ww1200/7119617822.jpg", "description": "Warm Taupe, кофейный, капучино, светло-бежевый, бежевый, кофе, тотал-беж, теплый бежевый", "price": 8826},
    {"title": "Джинсы DENIM STR", "photo": "https://ir-5.ozone.ru/s3/multimedia-1-a/wc1000/7184556550.jpg", "description": "утепленные.синий.04", "price": 2607}
]


@dp.message(Command("start"))
async def start(message: types.Message):
    """Обработка команды /start с отправкой списка товаров"""
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=[])  # Создаем клавиатуру с пустым списком

    for idx, product in enumerate(PRODUCTS):
        button = types.InlineKeyboardButton(
            text=product["title"],
            callback_data=f"buy_{idx}"
        )
        keyboard.inline_keyboard.append([button])  # Добавляем кнопку в виде строки

    await message.answer("Выберите товар для покупки:", reply_markup=keyboard)


@dp.callback_query(lambda c: c.data and c.data.startswith("buy_"))
async def process_buy(callback_query: types.CallbackQuery):
    """Обработка нажатия на кнопку покупки"""
    index = int(callback_query.data.split("_")[1])
    product = PRODUCTS[index]

    prices = [LabeledPrice(label=product["title"], amount=product["price"] * 100)]

    await bot.send_invoice(
        chat_id=callback_query.from_user.id,
        title=product["title"],
        photo_url=product["photo"],
        description=product["description"],
        payload=f"product_{index}",
        provider_token=PROVIDER_TOKEN,
        currency="RUB",
        prices=prices,
        start_parameter="test-payment",
    )
    await callback_query.answer()


@dp.pre_checkout_query(lambda query: True)
async def process_pre_checkout_query(pre_checkout_query: PreCheckoutQuery):
    """Подтверждение запроса на оплату"""
    await bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)


@dp.message(lambda message: message.successful_payment)
async def successful_payment(message: types.Message):
    """Обработка успешной оплаты"""
    await message.answer(
        f"Оплата прошла успешно! Спасибо за покупку")


async def main():
    """Запуск бота"""
    await dp.start_polling(bot)  # Передаем экземпляр бота в функцию


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except Exception as e:
        logging.error(f"Ошибка: {e}")