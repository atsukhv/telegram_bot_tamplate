from aiogram import Router, Bot, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, FSInputFile, CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession

import database.request as rq
router = Router()


@router.message(Command('start'))
async def start_command(message: Message, session: AsyncSession):
    await rq.set_user(message, session)
    await message.answer('Привет!')
