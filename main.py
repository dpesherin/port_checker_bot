from aiogram.utils import executor
from create_bot import dp
from handlers import other, admin

admin.register_handler_admin(dp)
other.register_handlers_other(dp)

executor.start_polling(dp, skip_updates = True)