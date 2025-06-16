"""
обработчики команд (основная логика)
"""
from aiogram.exceptions import TelegramAPIError
from aiogram.enums import ParseMode
import tempfile
import os
from db.requests import *
from aiogram.fsm.context import FSMContext
from aiogram import types
from bot.states import Form
from bot.keyboards import *
from bot.utils import *
from re import sub

async def start_controller(message: types.Message, state: FSMContext):
    """
    Обработка команды /start.
    :param message:
    :param state:
    :return:
    """
    user = await get_or_create_new_user(chat_id=message.chat.id, username=message.from_user.username, change_us=True)
    await message.answer("Это ремейк бота Джейсон Стетхэм, пока никакого функционала не реализовано")
