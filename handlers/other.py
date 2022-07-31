from email import message
from aiogram import Dispatcher, types
from create_bot import dp, bot

# @dp.message_handler()
async def on_message(message: types.Message):
    await bot.send_message(message.from_user.id, 'Напиши /start для отображения меню')
    print(message.from_user.id)

def register_handlers_other(dp : Dispatcher):
    dp.register_message_handler(on_message)