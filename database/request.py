from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession

from database.models import User

from sqlalchemy import select


async def set_user(message: Message, session: AsyncSession):
    user = await session.scalar(select(User).where(User.tg_id == message.from_user.id))
    if not user:
        session.add(User(tg_id=message.from_user.id))
        await session.commit()
