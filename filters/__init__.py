from aiogram import Dispatcher

from loader import dp
from .admin_filter import IsAdmin
from .group_filter import IsGroup
from .private import IsPrivate

if __name__ == "filters":
    dp.filters_factory.bind(IsAdmin)
    dp.filters_factory.bind(IsPrivate)
    dp.filters_factory.bind(IsGroup)