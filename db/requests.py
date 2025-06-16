"""
Функции для обращения к бд
"""
import random
from sqlalchemy import select, and_, or_, delete, update
from sqlalchemy.orm import joinedload
from sqlalchemy.sql import func
from sqlalchemy.ext.asyncio import AsyncSession
from db.async_session_generator import get_db
from db.models import *

async def get_or_create_new_user(chat_id: int, change_us: bool = False, username: str = None):
    """
    Принимает на вход id телеграм аккаунта и возвращает
    привязанного к нему пользователя (если его нет, создаёт).
    Если указать change_us = True, она обновит этому пользователю юзернейм
    :param chat_id: id аккаунта
    :param change_us: обновить ли юзернейм
    :param username: юзернейм
    :return: User
    """
    async with get_db() as db:
        result_db = await db.execute(select(User).where(User.id==chat_id))
        user = result_db.scalars().first()
        if user:
            if change_us:
                user.username = username
                await db.commit()
            return user
        if username is None:
            new_user = User(
                id=chat_id
            )
        else:
            new_user = User(
                id=chat_id,
                username=username
            )
        db.add(new_user)
        await db.commit()
        await db.refresh(new_user)
        return new_user


async def add_test_media(user_id: int, media: bytes, type: str, caption: str):
    """
    Добавляет в базу данных фото или видео пользователя,
    ещё не прошедшие модерацию
    :param user_id:
    :param media: байты файла
    :param type: тип (photo или video)
    :return:
    """
    async with get_db() as db:
        new_media = Media_test(
            user_id=user_id,
            file=media,
            media_type=type,
            caption = caption
        )
        db.add(new_media)
        await db.commit()


async def get_memes_count():
    async with get_db() as db:
        count = await db.execute(select(func.count(Media_test.id)))
        return count.scalar_one()


async def get_first_test_meme():
    async with get_db() as db:
        result = await db.execute(select(Media_test).options(
            joinedload(Media_test.user)
        ))
        media = result.scalars().first()
        return media


async def get_test_meme_by_id(id: int):
    async with get_db() as db:
        result = await db.execute(select(Media_test).where(Media_test.id == id))
        media = result.scalars().first()
        return media


async def add_media(user_id: int, media: bytes, type: str, caption: str):
    """
    Добавляет в базу данных фото или видео пользователя
    :param user_id:
    :param media: байты файла
    :param type: тип (photo или video)
    :return:
    """
    async with get_db() as db:
        new_media = Media(
            user_id=user_id,
            file=media,
            media_type=type,
            caption = caption
        )
        db.add(new_media)
        await db.commit()


async def delete_test_media(id: int):
    async with get_db() as db:
        await db.execute(delete(Media_test).where(
            Media_test.id==id
        ))
        await db.commit()


async def get_random_meme():
    async with get_db() as db:
        result = await db.execute(select(Media).order_by(func.random()).options(
            joinedload(Media.user)
        ))
        memes = result.scalars().all()
        return random.choice(memes) if memes else None


async def get_meme_likes_count(meme_id: int):
    async with get_db() as db:
        count = await db.execute(select(func.count(Like.id)).where(Like.media_id==meme_id))
        return count.scalar_one()


async def create_like(user_id: int, meme_id: int):
    async with get_db() as db:
        likes = await db.execute(select(Like).where(
            and_(
                Like.author_id == user_id,
                Like.media_id==meme_id
            )
        ))
        like = likes.scalars().first()
        if like:
            return
        new_like = Like(
            author_id=user_id,
            media_id=meme_id
        )
        db.add(new_like)
        await db.commit()


