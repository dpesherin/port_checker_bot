from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

kb_agreement = ReplyKeyboardMarkup()

yes = KeyboardButton(text='Сохранить')
no = KeyboardButton(text='Отменить')

kb_agreement.add(yes).add(no)