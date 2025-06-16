"""
Роуты (обработчики состояний) бота
"""
from aiogram import Router
from aiogram.filters import CommandStart, Command
from bot.command_controllers import *
from bot.states import Form
from aiogram.fsm.context import FSMContext
from aiogram import types

main_router = Router()

@main_router.message(CommandStart())
async def handle_start(message: types.Message, state: FSMContext):
    """
    Обрабатывает команду /start
    """
    return await start_controller(message, state)


