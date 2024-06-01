from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart

from data.db_query import create_user
from keyboards.default.add_birthday_button import add_birthday_button
from loader import dp


@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    await create_user(
        telegram_id=message.from_user.id,
        firstname=message.from_user.first_name,
        lastname=message.from_user.last_name,
        username=message.from_user.username,
        phone_number=None  # Assuming phone_number is optional
    )

    await message.answer(
        f"Assalomu Alaykum, {message.from_user.full_name}! Xush kelipsiz.\nTugilgan kun qo'shish uchun pastdagi tugmani bosing!",
        reply_markup=add_birthday_button)
