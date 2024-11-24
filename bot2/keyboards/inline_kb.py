from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

main_menu = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Добавить заметку", callback_data="add_note")],
    [InlineKeyboardButton(text="Просмотреть заметки", callback_data="view_notes")],
    [InlineKeyboardButton(text="Удалить заметку", callback_data="delete_note")],
])

def notes_buttons(notes: list):
    return InlineKeyboardMarkup(inline_keyboard=
                    [[InlineKeyboardButton(text=note, callback_data=f"del_note#{i}")] for i, note in enumerate(notes)]
    )