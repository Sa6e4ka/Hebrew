from aiogram import Router
from aiogram.filters import Command
from aiogram.types import  Message, FSInputFile
from Auxiliaries import button, error_handler

# Send Database Router
send_database_router = Router()


'''
Функция для отправки файла базы данных
'''
@send_database_router.message(Command("database"))
@error_handler
async def send_database_func(message: Message):
    file_info = FSInputFile("Database/base.db")
    await message.answer_document(document=file_info, caption="База данных со всеми таблицами и слсовами в ней", reply_markup=button(["Главное меню"]))