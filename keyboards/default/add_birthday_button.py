from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

add_birthday_button = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='📜Tugilgan Kun Qoshish')
        ],
    ],
    resize_keyboard=True
)

check_button = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='✅Togri'),
            KeyboardButton(text='❌Notogri'),
        ],
        [
            KeyboardButton(text='⏪Ortga'),
            KeyboardButton(text='❌Bekor Qilish'),

        ],

    ],
    resize_keyboard=True
)

check_image = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='❎Yoq'),
        ],
    ],
    resize_keyboard=True
)

check_text = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='❎Yoq'),
        ],
        [
            KeyboardButton(text='⏪Ortga'),
            KeyboardButton(text='❌Bekor Qilish'),
        ],
    ],
    resize_keyboard=True
)

cancel = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='❌Bekor Qilish'),
        ],
    ],
    resize_keyboard=True
)

back_button = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='⏪Ortga'),
            KeyboardButton(text='❌Bekor Qilish'),
        ],
    ],
    resize_keyboard=True
)
