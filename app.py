from aiogram import executor
import os
from loader import dp
from utils.notify_admins import on_startup_notify
from utils.set_bot_commands import set_default_commands

# Import Django and set it up
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'birthday.settings')
import django

django.setup()

# Import middlewares, filters, and handlers (assuming these modules are correctly defined)
import middlewares
import filters
import handlers


async def on_startup(dispatcher):
    # Set default bot commands (/start and /help)
    await set_default_commands(dispatcher)
    # Notify admins about bot startup
    await on_startup_notify(dispatcher)


if __name__ == '__main__':
    # Start the bot polling with on_startup function
    executor.start_polling(dp, on_startup=on_startup)
