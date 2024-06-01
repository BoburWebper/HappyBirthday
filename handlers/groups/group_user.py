from aiogram import types

from data.db_query import create_user
from filters import IsGroup
from loader import dp, bot


@dp.message_handler(IsGroup(), content_types=types.ContentTypes.NEW_CHAT_MEMBERS)
async def new_member(message: types.Message):
    members = ", ".join([m.get_mention(as_html=True) for m in message.new_chat_members])
    await message.reply(f"Xush Kelipsiz {members}.")
    await create_user(
        telegram_id=message.from_user.id,
        firstname=message.from_user.first_name,
        lastname=message.from_user.last_name,
        username=message.from_user.username,
        phone_number=None  # Assuming phone_number is optional
    )
    await message.reply(f"Assalomu Alaikum {message.from_user.first_name}!\nBizning guruhimizga Xush kelipsiz!")


@dp.message_handler(IsGroup(), content_types=types.ContentTypes.LEFT_CHAT_MEMBER)
async def left_member(message: types.Message):
    if message.left_chat_member.id == message.from_user.id:
        await message.answer(f"{message.left_chat_member.get_mention(as_html=True)} guruhni tark etdi")
    elif message.from_user.id == (await bot.me).id:
        return
    else:
        await message.answer(f"{message.from_user.full_name} guruhdan haydaldi"
                             f" Admin: {message.from_user.get_mention(as_html=True)}.")
