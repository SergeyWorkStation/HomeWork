import logging
import os
import asyncio
import aiohttp
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram import Bot, Dispatcher
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import Command, CommandStart

BOT_TOKEN = os.environ["TOKEN"]
SERVER_URL = 'http://localhost:8000'

logging.basicConfig(level=logging.INFO)


bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

class Form(StatesGroup):
   add_task = State()
   task_deadline = State()

@dp.message(CommandStart())
async def start_command(message: Message):
   await message.answer("Привет! Я бот для управления задачами. Используйте команды:\n/show_tasks, /add_task, /delete_task")

@dp.message(Command('show_tasks'))
async def show_tasks(message: Message):
   async with aiohttp.ClientSession() as session:
       async with session.get(f"{SERVER_URL}/tasks") as response:
           tasks = await response.json()
           if tasks:
               response_text = "\n".join([f"{task['id']}. {task['name']} (дедлайн: {task['deadline']})" for task in tasks])
           else:
               response_text = "Задач пока нет."
           await message.answer(response_text)

@dp.message(Command('add_task'))
async def add_task(message: Message, state: FSMContext):
   await message.answer("Введите название задачи:")
   await state.set_state(Form.add_task)


@dp.message(Form.add_task)
async def process_add_task(message: Message, state: FSMContext):
   await state.update_data(task_name= message.text)
   await message.answer("Введите дедлайн (ДД.ММ.ГГГГ):")
   await state.set_state(Form.task_deadline)


@dp.message(Form.task_deadline)
async def process_task_deadline(message: Message, state: FSMContext):
   await state.update_data(task_deadline = message.text)
   data = await state.get_data()
   async with aiohttp.ClientSession() as session:
       await session.post(f"{SERVER_URL}/tasks", json={"name": data['task_name'], "deadline": data['task_deadline']})
   await message.answer("Задача добавлена!")
   await state.clear()

@dp.message(Command('delete_task'))
async def delete_task(message: Message):
   async with aiohttp.ClientSession() as session:
       async with session.get(f"{SERVER_URL}/tasks") as response:
           tasks = await response.json()
           if tasks:
               keyboard = InlineKeyboardMarkup(inline_keyboard=[])
               for task in tasks:
                   keyboard.inline_keyboard.append([InlineKeyboardButton(text=f"Удалить {task['id']}",
                                                                         callback_data=f"delete_{task['id']}")])
               await message.answer("Выберите задачу для удаления:", reply_markup=keyboard)
           else:
               await message.answer("Задач для удаления нет.")

@dp.callback_query(lambda c: c.data.startswith('delete_'))
async def process_deletion(callback_query: CallbackQuery):
   task_id = int(callback_query.data.split('_')[1])
   async with aiohttp.ClientSession() as session:
       await session.delete(f"{SERVER_URL}/tasks/{task_id}")
   await callback_query.answer("Задача удалена!")
   await callback_query.message.edit_reply_markup()  # очищаем клавиатуру



async def main():
    """Запуск бота"""
    await dp.start_polling(bot)  # Передаем экземпляр бота в функцию


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except Exception as e:
        logging.error(f"Ошибка: {e}")