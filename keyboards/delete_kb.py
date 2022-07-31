from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

kb_del = ReplyKeyboardMarkup()

yes = KeyboardButton(text='Удалить')
no = KeyboardButton(text='Отменить')

kb_del.add(yes).add(no)