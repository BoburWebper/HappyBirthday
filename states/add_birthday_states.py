from aiogram.dispatcher.filters.state import StatesGroup, State


class AddBirthdayStates(StatesGroup):
    first_name = State()
    last_name = State()
    address = State()
    age = State()
    friends = State()
    close_friends = State()
    wishlist = State()
    phone_number = State()
    image = State()
    birthday = State()
    check_in = State()
    user_check_in = State()
    add_status = State()


class UpdateBirthday(StatesGroup):
    waiting_for_birthday_id = State()
