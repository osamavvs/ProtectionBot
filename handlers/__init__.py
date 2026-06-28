from . import admin, callbacks, locks, start
from aiogram import Dispatcher

def setup_routers(dp: Dispatcher):
    dp.include_routers(
        admin.router,
        callbacks.router,
        locks.router,
        start.router
    )
