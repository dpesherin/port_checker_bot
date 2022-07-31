from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

b2 = KeyboardButton('/Добавить_задачу')
b3 = KeyboardButton('/Удалить_задачу')
b4 = KeyboardButton('/Показать_задачи')
b5 = KeyboardButton('/Регистрация')

kb_admin = ReplyKeyboardMarkup(resize_keyboard=True)
kb_admin.add(b2).add(b3).add(b4).add(b5)