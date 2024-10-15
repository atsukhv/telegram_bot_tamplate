from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove, InlineKeyboardMarkup, InlineKeyboardButton
from sqlalchemy.ext.asyncio import AsyncSession

import database.request as rq

router = Router()


@router.message(Command('start'))
async def start_command(message: Message, session: AsyncSession):
    # await rq.set_user(message, session)  # Запись пользователя в БД
    await message.answer('Безопасная плазма ведет к щиту.', reply_markup=test_kb)
    await message.delete(1)


test_kb = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='Тест', callback_data='test')]])


@router.callback_query(F.data == 'test')
async def test_callback(call: CallbackQuery):
    await call.message.answer('Subspace test.')
