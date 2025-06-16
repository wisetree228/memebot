"""
клавиатуры бота
"""
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

menu_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Добавить мем", callback_data="add_meme")],
    [InlineKeyboardButton(text="Листать мемы", callback_data="watch_memes")]
])

async def get_admin_keyboard(memes_count: int):
    admin_keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Добавить мем", callback_data="add_meme")],
        [InlineKeyboardButton(text="Листать мемы", callback_data="watch_memes")],
        [InlineKeyboardButton(text=f"Новых мемов: {memes_count}", callback_data="moderate")]
    ])
    return admin_keyboard


accept_or_not_keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Одобрить", callback_data="good"), InlineKeyboardButton(text="Не одобрить", callback_data="bad")]
])

like_keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Лайк", callback_data="like"), InlineKeyboardButton(text="Игнор", callback_data="dislike")]
])