"""
Состояния обработки бота
"""
from aiogram.fsm.state import StatesGroup, State


class Form(StatesGroup):
    """
    Состояния обработки для бота
    """
    add_meme = State()