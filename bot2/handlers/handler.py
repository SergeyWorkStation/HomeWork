from aiogram import Router
from aiogram.filters import Command, CommandStart, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from bot2.keyboards import inline_kb as kb
from bot2.states.state_bot import BotStates

router = Router()

notes = []


@router.message(CommandStart())
async def welcome(message: Message, state: FSMContext):
    await message.answer(f"Здравствуйте, {message.from_user.full_name}, Введите команду /test")
    await state.set_state(BotStates.start)


@router.message(StateFilter(BotStates.start), Command("test"))
async def test(message: Message):
    await message.answer('Выберите действие:', reply_markup=kb.main_menu)


@router.callback_query(lambda query: query.data == 'add_note')
async def add_note(query: CallbackQuery, state: FSMContext):
    await query.answer()
    await state.update_data(start=query.data)
    await query.message.answer("Введите текст вашей заметки:")
    await state.set_state(BotStates.add_note)


@router.message(StateFilter(BotStates.add_note))
async def add_notes(message: Message, state: FSMContext):
    notes.append(message.text)
    await message.answer("Заметка добавлена")
    await state.set_state(BotStates.start)
    await test(message)


@router.callback_query(lambda query: query.data == 'view_notes')
async def view_note(query: CallbackQuery, state: FSMContext):
    await query.answer()
    await query.message.answer("Ваши заметки:\n" + ''.join(f'{i+1}. {note}\n' for i, note in enumerate(notes)))
    await state.set_state(BotStates.start)
    await test(query.message)


@router.callback_query(lambda query: query.data == 'delete_note')
async def del_note(query: CallbackQuery, state: FSMContext):
    await query.answer()
    await query.message.answer("Выберите заметку для удаления", reply_markup=kb.notes_buttons(notes))
    await state.set_state(BotStates.delete_note)


@router.callback_query(lambda query: query.data.split('#')[0] == 'del_note', StateFilter(BotStates.delete_note))
async def add_note(query: CallbackQuery, state: FSMContext):
    await query.answer()
    notes.pop(int(query.data.split('#')[1]))
    await query.message.answer(f"Заметка № {int(query.data.split('#')[1])+1} удалена")
    await state.set_state(BotStates.start)
    await test(query.message)
