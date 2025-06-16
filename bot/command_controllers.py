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

ADMINS_ID = os.getenv("ADMINS_ID").split(',')

async def start_controller(message: types.Message, state: FSMContext):
    """
    Обработка команды /start. Даёт пользователю главное меню
    :param message:
    :param state:
    :return:
    """
    await get_or_create_new_user(chat_id=message.chat.id, username=message.from_user.username, change_us=True)
    if str(message.chat.id) in ADMINS_ID:
        await message.answer(f"Это ремейк бота Джейсон Стетхэм, тут можно выкладывать и лайкать мемы!",
                             reply_markup=await get_admin_keyboard(await get_memes_count()))
        return
    await message.answer(f"Это ремейк бота Джейсон Стетхэм, тут можно выкладывать и лайкать мемы!", reply_markup=menu_keyboard)


async def add_meme_controller(callback: types.CallbackQuery, state: FSMContext):
    """
    Обрабатывает кнопку 'добавить мем'
    """
    await get_or_create_new_user(chat_id=callback.message.chat.id, change_us=True, username=callback.message.from_user.username)
    await callback.message.edit_text("Отправьте фото или видео, можно с текстом:")
    await state.set_state(Form.add_meme)


async def add_media_controller(message: types.Message, state: FSMContext):
    """
    Принимает мем от пользователя и отправляет на модерацию
    """
    if not message.photo and not message.video:
        await message.answer('Отправьте картинку и/или видео, другой формат информации не принимается!', reply_markup=menu_keyboard)
        await state.set_state(Form.add_meme)
        return
    else:
        total_files = 0
        if message.photo:
            total_files += 1
        if message.video:
            total_files += 1

        if total_files > 1:
            await message.answer('Максимум 1 файл!')
            await state.set_state(Form.add_meme)
            return
        else:
            bot = message.bot

            if message.photo:
                largest_photo = message.photo[-1]
                file_id = largest_photo.file_id
                file = await bot.get_file(file_id)
                photo = await bot.download_file(file.file_path)
                photo_bytes = photo.read()
                if not( message.caption ):
                    caption = None
                else:
                    caption = message.caption
                await add_test_media(user_id=message.chat.id, media=photo_bytes, type='photo', caption=caption)

            if message.video:
                file_id = message.video.file_id
                file = await bot.get_file(file_id)
                video = await bot.download_file(file.file_path)
                video_bytes = video.read()
                if not( message.caption ):
                    caption = None
                else:
                    caption = message.caption
                await add_test_media(user_id=message.chat.id, media=video_bytes, type='video', caption=caption)
        if str(message.chat.id) in ADMINS_ID:
            await message.answer(
                'Ваш мемасик отправлен на модерацию админу',
                reply_markup=await get_admin_keyboard(await get_memes_count()))
            await state.clear()
            return
        await message.answer(
            'Ваш мемасик отправлен на модерацию админу',
            reply_markup=menu_keyboard)
        await state.clear()


async def moderate_controller(callback: types.CallbackQuery, state: FSMContext):
    """
    Обрабатывает кнопку админа "смотреть предложку"
    """
    if not( str(callback.message.chat.id) in ADMINS_ID ):
        await callback.message.edit_text("Вы не админ!", reply_markup=menu_keyboard)
        return
    meme = await get_first_test_meme()
    if meme is None:
        await callback.message.bot.send_message(chat_id=callback.message.chat.id, text="Нету мемов", reply_markup=await get_admin_keyboard(await get_memes_count()))
    if not(meme.caption):
        caption = ""
    else:
        caption = meme.caption
    user = await get_or_create_new_user(chat_id=meme.user_id)
    if user.username:
        link = f'https://t.me/{user.username}'
    else:
        link = f'tg://user?id={user.id}'
    await send_media_group_with_caption(media_items=[meme], caption=caption, bot = callback.message.bot, chat_id=callback.message.chat.id)
    if user.username:
        text = f'<b>Автор мема:</b><a href="{link}">{user.username}</a>\n<b>Если ссылка на профиль не работает, проблема в том что пользователь установил такие настройки конфиденциальности</b>'
    else:
        text = f'<b>Автор мема:</b><a href="{link}">(No username)</a>\n<b>Если ссылка на профиль не работает, проблема в том что пользователь установил такие настройки конфиденциальности</b>'
    await callback.message.bot.send_message(chat_id=callback.message.chat.id, text=text, parse_mode=ParseMode.HTML)
    await state.update_data(meme_id=meme.id)
    await callback.message.bot.send_message(chat_id=callback.message.chat.id, text="Оценочку:", reply_markup=accept_or_not_keyboard)


async def good_meme_controller(callback: types.CallbackQuery, state: FSMContext):
    """
    Обрабатывает одобрение мема админом
    """
    data = await state.get_data()
    id = data.get('meme_id')
    media = await get_test_meme_by_id(id)
    await add_media(user_id=media.user_id, media=media.file, type=media.media_type, caption=media.caption)
    await delete_test_media(id)
    await send_media_group_with_caption(media_items=[media], caption="ВАШ МЕМ ОДОБРЕН!", bot=callback.message.bot, chat_id=media.user_id)
    await callback.message.bot.send_message(chat_id=media.user_id, text='Выберите дальнейшую опцию',
                                            reply_markup=menu_keyboard)
    await callback.message.bot.send_message(chat_id=callback.message.chat.id, text="Одобрено!", reply_markup=await get_admin_keyboard(await get_memes_count()))
    data.pop('meme_id')
    await state.update_data(**data)


async def bad_meme_controller(callback: types.CallbackQuery, state: FSMContext):
    """
    Обрабатывает неодобрение мема админом
    """
    data = await state.get_data()
    id = data.get('meme_id')
    media = await get_test_meme_by_id(id)
    await delete_test_media(id)
    await send_media_group_with_caption(media_items=[media], caption="ваш мем НЕ одобрен(", bot=callback.message.bot,
                                        chat_id=media.user_id)
    await callback.message.bot.send_message(chat_id=media.user_id, text='Выберите дальнейшую опцию', reply_markup=menu_keyboard)
    await callback.message.bot.send_message(chat_id=callback.message.chat.id, text="Не одобрено!",
                                            reply_markup=await get_admin_keyboard(await get_memes_count()))
    data.pop('meme_id')
    await state.update_data(**data)


async def watch_meme_controller(callback: types.CallbackQuery, state: FSMContext):
    """
    Обрабатывает кнопку "листать мемы"
    """
    await get_or_create_new_user(chat_id=callback.message.chat.id, change_us=True,
                                 username=callback.message.from_user.username)
    meme = await get_random_meme()
    if meme is None:
        if str(callback.message.chat.id) in ADMINS_ID:
            await callback.message.bot.send_message(chat_id=callback.message.chat.id, text="Нету мемов",
                                                reply_markup=await get_admin_keyboard(await get_memes_count()))
        else:
            await callback.message.bot.send_message(chat_id=callback.message.chat.id, text="Нету мемов",
                                                    reply_markup=menu_keyboard)

        return
    user = meme.user
    caption_add = f"\n\nНа этом меме {await get_meme_likes_count(meme.id)} лайков"
    await send_media_group_with_caption(media_items=[meme], caption=meme.caption+caption_add, bot=callback.message.bot, chat_id=callback.message.chat.id)
    if user.username:
        link = f'https://t.me/{user.username}'
    else:
        link = f'tg://user?id={user.id}'
    if user.username:
        text = f'<b>Автор мема:</b><a href="{link}">{user.username}</a>\n<b>Если ссылка на профиль не работает, проблема в том что пользователь установил такие настройки конфиденциальности</b>'
    else:
        text = f'<b>Автор мема:</b><a href="{link}">(No username)</a>\n<b>Если ссылка на профиль не работает, проблема в том что пользователь установил такие настройки конфиденциальности</b>'
    await callback.message.bot.send_message(chat_id=callback.message.chat.id, text=text, parse_mode=ParseMode.HTML)
    await state.update_data(mm_id=meme.id)
    await callback.message.bot.send_message(chat_id=callback.message.chat.id, text="Оцените мем:", reply_markup=like_keyboard)


async def like_meme_controller(callback: types.CallbackQuery, state: FSMContext):
    """
    Обрабатывает лайк на мем
    """
    data = await state.get_data()
    mm_id = data.get('mm_id')
    await create_like(callback.message.chat.id, mm_id)
    data.pop('mm_id')
    await state.update_data(**data)
    if str(callback.message.chat.id) in ADMINS_ID:
        await callback.message.bot.send_message(chat_id=callback.message.chat.id,
                                                text="Лайк записан!", reply_markup=await get_admin_keyboard(await get_memes_count()))
        return
    await callback.message.bot.send_message(chat_id=callback.message.chat.id, text="Лайк записан!", reply_markup=menu_keyboard)


async def dislike_meme_controller(callback: types.CallbackQuery, state: FSMContext):
    """
    Обрабатывает дизлайк (не совсем дизлайк, просто игнор вместо лайка) на мем
    """
    data = await state.get_data()
    data.pop('mm_id')
    await state.update_data(**data)
    if str(callback.message.chat.id) in ADMINS_ID:
        await callback.message.bot.send_message(chat_id=callback.message.chat.id,
                                                text="Хорошо, выберите дальнейшую опцию", reply_markup=await get_admin_keyboard(await get_memes_count()))
        return
    await callback.message.bot.send_message(chat_id=callback.message.chat.id, text="Хорошо, выберите дальнейшую опцию", reply_markup=menu_keyboard)


