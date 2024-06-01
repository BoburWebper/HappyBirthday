import logging
import os
from datetime import datetime

import django
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardRemove, InputFile, ContentType
from asgiref.sync import sync_to_async
from django.core.files.base import ContentFile

from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError

from keyboards.default.add_birthday_button import check_button, check_image, check_text, cancel, back_button, \
    add_birthday_button
from utils.cheack_phoneNum import is_valid_phone_number

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'birthday.settings')
django.setup()
from config.models import Users, UserBirthdays, UserBirthdayImages, Advertisement, Card

ADMINS = os.getenv("ADMINS")
from loader import dp, bot
from states.add_birthday_states import AddBirthdayStates, UpdateBirthday


@dp.message_handler(text='📜Tugilgan Kun Qoshish')
async def add_birthday(message: types.Message, state: FSMContext):
    await message.answer(
        """
<b>Tug'ilgan kun qo'shish uchun ba'zi savollarimizga javob berishingizni iltimos qilamiz.</b>
<b>Tug'ilgan kun egasining ismini kiriting!</b>
<code>Misol uchun: Bobur</code>
        """,
        parse_mode="HTML", reply_markup=cancel
    )
    await state.set_state(AddBirthdayStates.first_name)


@dp.message_handler(state=AddBirthdayStates.first_name)
async def get_lastname(message: types.Message, state: FSMContext):
    if message.text == "❌Bekor Qilish":
        await state.finish()
        await message.answer("Jarayon toxtatildi!", reply_markup=add_birthday_button)
    else:
        await state.update_data(first_name=message.text)
        await message.answer("<b>Tugilgan Kun egasining familiyasini kiriting.</b>", parse_mode="HTML",
                             reply_markup=back_button)
        await state.set_state(AddBirthdayStates.last_name)


@dp.message_handler(state=AddBirthdayStates.last_name)
async def get_lastname(message: types.Message, state: FSMContext):
    if message.text == "❌Bekor Qilish":
        await state.finish()
        await state.reset_data()
        await message.answer("Jarayon toxtatildi!", reply_markup=add_birthday_button)
    elif message.text == "⏪Ortga":
        await state.set_state(AddBirthdayStates.first_name)
        await message.answer("<b>Tug'ilgan kun egasining ismini kiriting!</b>\n<code>Misol uchun: Bobur</code>",
                             parse_mode="HTML", reply_markup=cancel)
    else:
        await state.update_data(last_name=message.text)
        await message.answer(
            "Tugilgan kun egasining addresini kiriting.\n<code>Misol uchun: Toshkent shahri</code>",
            parse_mode="HTML", reply_markup=back_button)
        await state.set_state(AddBirthdayStates.address)


@dp.message_handler(state=AddBirthdayStates.address)
async def get_lastname(message: types.Message, state: FSMContext):
    if message.text == '❌Bekor Qilish':
        await message.answer("Jarayon bekor qilindi", reply_markup=add_birthday_button)
        await state.finish()
        await state.reset_data()
    elif message.text == '⏪Ortga':
        await message.answer("<b>Tugilgan Kun egasining familiyasini kiriting.</b>", parse_mode="HTML",
                             reply_markup=back_button)
        await state.set_state(AddBirthdayStates.last_name)
    else:
        await state.update_data(address=message.text)
        await message.answer(
            "Tugilgan kun egasining yoshini kiriting nechi yoshga kiradi.\n<code>Misol uchun: 21</code>",
            parse_mode="HTML", reply_markup=back_button)
        await state.set_state(AddBirthdayStates.age)


@dp.message_handler(state=AddBirthdayStates.age)
async def get_age(message: types.Message, state: FSMContext):
    if message.text == '❌Bekor Qilish':
        await message.answer("Jarayon toxtatildi", reply_markup=add_birthday_button)
        await state.finish()
        await state.reset_data()
    elif message.text == '⏪Ortga':
        await message.answer(
            "Tugilgan kun egasining addresini kiriting.\n<code>Misol uchun: Toshkent shahri</code>",
            parse_mode="HTML", reply_markup=back_button)
        await state.set_state(AddBirthdayStates.address)
    else:
        try:
            age = int(message.text)
            await state.update_data(age=age)
            await message.answer(
                "Tabrik kimlar tomonidan.\n<code>Misol uchun: Do'stlari (ismlari bolsa yaxshi boladi)</code>",
                parse_mode="HTML", reply_markup=back_button
            )
            await state.set_state(AddBirthdayStates.friends)
        except ValueError:
            await message.reply("<b>Iltimos yoshni tog'ri kiriting</b>", parse_mode="HTML")


@dp.message_handler(state=AddBirthdayStates.friends)
async def get_friends(message: types.Message, state: FSMContext):
    if message.text == '❌Bekor Qilish':
        await message.answer("Jarayon toxtatildi", reply_markup=add_birthday_button)
        await state.finish()
        await state.reset_data()
    elif message.text == '⏪Ortga':
        await message.answer(
            "Tugilgan kun egasining yoshini kiriting nechi yoshga kiradi.\n<code>Misol uchun: 21</code>",
            parse_mode="HTML", reply_markup=back_button)
        await state.set_state(AddBirthdayStates.age)
    else:

        await state.update_data(friends=message.text)
        await message.answer("<b>Tabrik aynan kim tomonidan.</b>\n<code>Misol uchun: Suhrob do'sti tomonidan</code>",
                             parse_mode="HTML", reply_markup=back_button)
        await state.set_state(AddBirthdayStates.close_friends)


@dp.message_handler(state=AddBirthdayStates.close_friends)
async def close_friends(message: types.Message, state: FSMContext):
    if message.text == '❌Bekor Qilish':
        await message.answer("Jarayon toxtatildi", reply_markup=add_birthday_button)
        await state.finish()
        await state.reset_data()
    elif message.text == '⏪Ortga':
        await message.answer(
            "Tabrik kimlar tomonidan.\n<code>Misol uchun: Do'stlari (ismlari bolsa yaxshi boladi)</code>",
            parse_mode="HTML", reply_markup=back_button
        )
        await state.set_state(AddBirthdayStates.friends)
    else:
        await state.update_data(close_friends=message.text)
        await message.answer(
            "Tabrik xatini bolsa kiriting.\n<code>Misol uchun: Yozilgan sher bolishi mumkin yoki tilaklaringiz.</code>\n<b>Bor bolsa yuboring\nYoq bolsa Yoq tugmasini bosing.</b>",
            parse_mode='HTML', reply_markup=check_text)
        await state.set_state(AddBirthdayStates.wishlist)


@dp.message_handler(state=AddBirthdayStates.wishlist)
async def wishlist(message: types.Message, state: FSMContext):
    if message.text == "❌Bekor Qilish":
        await message.answer("Jarayon toxtatildi", reply_markup=add_birthday_button)
        await state.finish()
        await state.reset_data()
    elif message.text == "⏪Ortga":
        await message.answer("<b>Tabrik aynan kim tomonidan.</b>\n<code>Misol uchun: Suhrob do'sti tomonidan</code>",
                             parse_mode="HTML", reply_markup=back_button)
        await state.set_state(AddBirthdayStates.close_friends)
    else:
        if message.text == '❎Yoq':
            await state.update_data(wishlist=None)
            await message.answer(
                "Biz boglanishimiz uchun.Tugilgan kun egasining Telefon raqamini kiriting.\n<code>Misol uchun (+998991363884).</code>\n<b>Iltimos joy tashlamasdan yozing</b>",
                parse_mode='HTML', reply_markup=back_button)
            await state.set_state(AddBirthdayStates.phone_number)
        else:
            await state.update_data(wishlist=message.text)
            await message.answer(
                "Biz boglanishimiz uchun.Tugilgan kun egasining Telefon raqamini kiriting.\n<code>Misol uchun (+998991363884).</code>\n<b>Iltimos joy tashlamasdan yozing</b>",
                parse_mode='HTML', reply_markup=back_button)
            await state.set_state(AddBirthdayStates.phone_number)


@dp.message_handler(state=AddBirthdayStates.phone_number)
async def phone_number(message: types.Message, state: FSMContext):
    if message.text == '❌Bekor Qilish':
        await message.answer("Jarayon toxtatildi", reply_markup=add_birthday_button)
        await state.finish()
        await state.reset_data()
    elif message.text == '⏪Ortga':
        await message.answer(
            "Tabrik xatingiz bolsa kiriting.\n<code>Misol uchun: Yozilgan sher bolishi mumkin yoki tilaklaringiz.</code>\n<b>Bor bolsa yuboring\nYoq bolsa Yoq tugmasini bosing.</b>",
            parse_mode='HTML', reply_markup=check_text)
        await state.set_state(AddBirthdayStates.wishlist)
    else:
        phone_number = message.text
        try:
            if is_valid_phone_number(phone_number):
                await state.update_data(phone_number=message.text)
                await message.answer(
                    """<b>Tugilgan kunni kiriting</b>.\n<code>Masalan (2009-09-09)</code>""", parse_mode='HTML',
                    reply_markup=back_button)
                await state.set_state(AddBirthdayStates.birthday)

            else:
                await message.reply("<code>Iltimos telefon raqmani +998991363884 korinishida kiriting</code>",
                                    parse_mode='HTML', reply_markup=back_button)
        except Exception as e:
            await message.answer("<b>Iltimos Togri raqam kiriting</b>", parse_mode='HTML', reply_markup=back_button)


@dp.message_handler(state=AddBirthdayStates.birthday)
async def process_birthday(message: types.Message, state: FSMContext):
    if message.text == "❌Bekor Qilish":
        await message.answer("Jarayon toxtatildi", reply_markup=add_birthday_button)
        await state.finish()
        await state.reset_data()
    elif message.text == "⏪Ortga":
        await message.answer(
            "Biz boglanishimiz uchun.Tugilgan kun egasining Telefon raqamini kiriting.\n<code>Misol uchun (+998991363884).</code>\n<b>Iltimos joy tashlamasdan yozing</b>",
            parse_mode='HTML', reply_markup=back_button)
        await state.set_state(AddBirthdayStates.phone_number)
    else:
        try:
            birthday = datetime.strptime(message.text, '%Y-%m-%d').date()
            async with state.proxy() as data:
                data['birthday'] = birthday

            await message.answer(
                "<b>Kiritilgan Barcha malumotlar togrimi</b>")
            await bot.send_message(chat_id=message.from_user.id, text=f"""
    Ismi: {data['first_name']}
    Familiysi: {data['last_name']}
    Manzili: {data['address']}
    Yoshi: {data['age']}
    Kimlar tomonidanL: {data['friends']}
    Kim tomonidan : {data['close_friends']}
    Tabriknoma: {data['wishlist']}
    Telefon raqmi: {data['phone_number']}
    Tugilgan sanasi: {data['birthday']}""", parse_mode="HTML", reply_markup=check_button)
            await AddBirthdayStates.check_in.set()
        except ValueError:
            await message.answer(
                "<b>Iltimos, qaytadan kiriting.</b> <code>Masalan (2009-12-28) yani (yil-oy-kun).</code>",
                parse_mode="HTML")
        except IntegrityError:
            await message.answer("An error occurred while saving the data. Please try again.")


@dp.message_handler(state=AddBirthdayStates.check_in)
async def check_in(message: types.Message, state: FSMContext):
    if message.text == "❌Bekor Qilish":
        await message.answer("Jarayon toxtatildi", reply_markup=add_birthday_button)
        await state.finish()
        await state.reset_data()
    elif message.text == "⏪Ortga":
        await message.answer(
            """<b>Tugilgan kunni kiriting</b>.\n<code>Masalan (2009-09-09)</code>""", parse_mode='HTML',
            reply_markup=back_button)
        await state.set_state(AddBirthdayStates.birthday)
    else:
        if message.text == '✅Togri':
            try:
                async with state.proxy() as data:
                    telegram_user_id = message.from_user.id

                    # Wrap the synchronous ORM operation in sync_to_async
                    user, created = await sync_to_async(Users.objects.get_or_create)(telegram_id=telegram_user_id)

                    # Create UserBirthdays entry
                    user_birthday = await sync_to_async(UserBirthdays.objects.create)(
                        telegram_id=user,
                        first_name=data['first_name'],
                        last_name=data['last_name'],
                        address=data['address'],
                        age=data['age'],
                        friends=data['friends'],
                        close_friends=data['close_friends'],
                        wishlist=data['wishlist'],
                        phone_number=data['phone_number'],
                        birthday=data['birthday']
                    )

                    # Store the birthday_id in the state
                    data['birthday_id'] = user_birthday.birthday_id
                    print(data['birthday_id'])
                    await state.set_state(AddBirthdayStates.image)
                    await message.answer('<b>Video yasashimiz uchun rasmlari bolsa tashlashingiz mumkin!\n'
                                         'Agar rasm yoq bolsa Yoq tugmasini bosing.Bor bolsa tashlang</b>',
                                         parse_mode="HTML",
                                         reply_markup=check_image)
            except IntegrityError:
                await message.answer("An error occurred while saving the data. Please try again.")

        elif message.text == '❌Notogri':
            await message.answer("Boshdan kettik")
            await message.reply("<b>Tug'ilgan kun egasining ismini kiriting!</b>\n<code>Misol uchun: Bobur</code>",
                                reply_markup=cancel)
            await state.set_state(AddBirthdayStates.first_name)


@dp.message_handler(content_types=[ContentType.PHOTO, ContentType.TEXT],
                    state=AddBirthdayStates.image)
async def handle_image_or_text(message: types.Message, state: FSMContext):
    if message.text and message.text.lower() == '❎yoq':  # Handle 'Yoq' command
        await handle_yoq_command(message, state)
    elif message.photo:  # Handle photo upload
        await handle_photo_upload(message, state)
    elif message.text and message.text.lower() == 'finish':  # Handle 'Finish' command
        await finish_images(message, state)


async def handle_yoq_command(message: types.Message, state: FSMContext):
    objects = await sync_to_async(list)(Card.objects.all())
    for obj in objects:
        if obj.cardInfo:
            await message.answer(f"<b>Barcha malumotlar adminga yuborildi.\n{obj.cardInfo}</b>", parse_mode="HTML",
                                 reply_markup=ReplyKeyboardRemove())
    await state.set_state(AddBirthdayStates.user_check_in)


async def handle_photo_upload(message: types.Message, state: FSMContext):
    image_file_id = message.photo[-1].file_id
    file_info = await bot.get_file(image_file_id)
    file_content = await bot.download_file(file_info.file_path)

    # Convert BytesIO to bytes
    file_bytes = file_content.read()

    async with state.proxy() as data:
        if 'images' not in data:
            data['images'] = []
        data['images'].append(image_file_id)

        # Save the image to the Django model using sync_to_async
        telegram_user_id = message.from_user.id

        user = await sync_to_async(Users.objects.get)(telegram_id=telegram_user_id)
        birthday_id = data['birthday_id']
        user_birthday = await sync_to_async(UserBirthdays.objects.get)(birthday_id=birthday_id)

        image_instance = UserBirthdayImages(user_birthday=user_birthday)

        # Use sync_to_async to save the image asynchronously
        await sync_to_async(image_instance.image.save)(f"{image_file_id}.jpg", ContentFile(file_bytes))

    await message.answer("Rasm qoshildi")
    await message.answer(
        "<b>Rasm Qo'shishingiz mumkin, faqat 10 tadan oshmasin.</b>\nOxirida <code>Finish</code> ni bosing",
        parse_mode="HTML",
        reply_markup=types.ReplyKeyboardMarkup(
            keyboard=[[types.KeyboardButton(text="Finish")]],
            resize_keyboard=True
        ))


# Separate handler for the 'Finish' command
async def finish_images(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        if 'images' in data and data['images']:
            await message.answer("Saqlandi")
        else:
            await message.answer("Hech qanday rasm qo'shilmagan.")
    await send_card_info_to_admin(message)
    await state.set_state(AddBirthdayStates.user_check_in)


async def send_card_info_to_admin(message):
    objects = await sync_to_async(list)(Card.objects.all())
    for obj in objects:
        if obj.cardInfo:
            await message.answer(f"<b>Barcha malumotlar adminga yuborildi.\n{obj.cardInfo}</b>", parse_mode="HTML",
                                 reply_markup=ReplyKeyboardRemove())


@dp.message_handler(content_types=types.ContentType.PHOTO, state=AddBirthdayStates.user_check_in)
async def check_out(message: types.Message, state: FSMContext):
    data = await state.get_data()
    photo = message.photo[-1]  # Get the highest resolution photo
    file_id = photo.file_id

    await bot.send_photo(chat_id=ADMINS, photo=file_id,
                         caption=f"Tolov cheki.\nAgar togri bolsa /update_birthday ga ID ni  yuboring.\nBirthday id: {data['birthday_id']}")

    await bot.send_message(chat_id=ADMINS, text=f"""Yangi Tugilgan kun
Ismi: {data['first_name']}
Familiysi: {data['last_name']}
Manzili: {data['address']}
Yoshi: {data['age']}
Kimlar tomonidanL: {data['friends']}
Kim tomonidan : {data['close_friends']}
Tabriknoma: {data['wishlist']}
Telefon raqmi: {data['phone_number']}
Tugilgan sanasi: {data['birthday']}""")
    await state.finish()


# Command to start the birthday ID update process
@dp.message_handler(lambda message: message.from_user.id == int(ADMINS), commands=['update_birthday'])
async def start_update_birthday(message: types.Message):
    await message.reply("Tolov cheki togri bolsa Birthday Id ni yuboring!")
    await UpdateBirthday.waiting_for_birthday_id.set()


# Handler to receive the birthday ID and update the database
@dp.message_handler(lambda message: message.from_user.id == int(ADMINS),
                    state=UpdateBirthday.waiting_for_birthday_id)
async def add_birthday(message: types.Message, state: FSMContext):
    birthday_id = message.text
    try:
        user_birthday = await sync_to_async(UserBirthdays.objects.get)(pk=birthday_id)
        user_birthday.payment_status = True
        await sync_to_async(user_birthday.save)()
        await message.answer("Payment status updated successfully.")
    except ObjectDoesNotExist:
        await message.answer("User birthday not found in the database.")
    except ValueError:
        await message.answer("Invalid ID. Please send a valid birthday ID.")
    finally:
        await state.finish()


@dp.message_handler(commands=['reklama'])
async def advertising(message: types.Message):
    # Only proceed if the message is from an admin
    if message.from_user.id == int(ADMINS):
        users = await sync_to_async(list)(Users.objects.all())
        advertisements = await sync_to_async(list)(Advertisement.objects.all())

        for user in users:
            if user.telegram_id:
                for ad in advertisements:
                    try:
                        if ad.image:
                            await bot.send_photo(chat_id=user.telegram_id, photo=InputFile(ad.image.path),
                                                 caption=ad.text)
                        elif ad.video:
                            await bot.send_video(chat_id=user.telegram_id, video=InputFile(ad.video.path),
                                                 caption=ad.text)
                        else:
                            await bot.send_message(chat_id=user.telegram_id, text=ad.text)
                    except Exception as e:
                        logging.error(f"Error sending advertisement {ad.id} to user {user.telegram_id}: {e}")
