"""
Роуты (обработчики состояний) бота
"""
from aiogram import Router, F
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


@main_router.callback_query(F.data == "add_meme")
async def process_add_meme(callback: types.CallbackQuery, state: FSMContext):
    return await add_meme_controller(callback, state)


@main_router.message(Form.add_meme)
async def add_meme(message: types.Message, state: FSMContext):
    return await add_media_controller(message, state)


@main_router.callback_query(F.data == "moderate")
async def process_moderate(callback: types.CallbackQuery, state: FSMContext):
    return await moderate_controller(callback, state)


@main_router.callback_query(F.data == "good")
async def process_good_meme(callback: types.CallbackQuery, state: FSMContext):
    return await good_meme_controller(callback, state)


@main_router.callback_query(F.data == "bad")
async def process_bad_meme(callback: types.CallbackQuery, state: FSMContext):
    return await bad_meme_controller(callback, state)


@main_router.callback_query(F.data == "watch_memes")
async def watch_random_meme(callback: types.CallbackQuery, state: FSMContext):
    return await watch_meme_controller(callback, state)


@main_router.callback_query(F.data == "like")
async def like_meme(callback: types.CallbackQuery, state: FSMContext):
    return await like_meme_controller(callback, state)


@main_router.callback_query(F.data == "dislike")
async def dislike_meme(callback: types.CallbackQuery, state: FSMContext):
    return await dislike_meme_controller(callback, state)