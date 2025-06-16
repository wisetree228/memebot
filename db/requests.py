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


