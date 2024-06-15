'''
Хендлеры приветствия и кнопок перехода в главное меню
'''
from aiogram import F, Router
from aiogram.filters import CommandStart, StateFilter, or_f, Command
from aiogram.fsm.context import FSMContext
from aiogram.types import  Message, CallbackQuery
 
from sqlalchemy.ext.asyncio import AsyncSession
from Database import orm_add_user
from Auxiliaries import hello, command_list, StartKB, error_handler


# Start Router
start_router = Router()


'''
Обработчик команды старт
'''
@start_router.message(StateFilter(None) ,CommandStart())
@error_handler
async def start(message : Message, session : AsyncSession):
    # Сохранение пользователя в таблице
    if message.from_user.username is not None:
        await orm_add_user(session=session, username=message.from_user.username, chat_id=message.chat.id)
        await message.answer(text= hello, reply_markup=StartKB.as_markup())
        return
    await message.answer(text="<b>Пожалуйста, добавьте в своем профиле telegram имя пользователя (поле Username) иначе вам будет недоступен функционал бота!\n\nПосле этого обязательно введите команду /start еще раз!</b>")


'''
Обработчик кнопки для перехода в главное меню
'''
@start_router.callback_query(or_f(F.data == "Главное меню", F.data == "Отмена"))
@error_handler
async def start_on_button(call : CallbackQuery, state: FSMContext):
    await state.clear()
    if call.message.text:
        await call.message.edit_text(text= command_list,reply_markup=StartKB.as_markup())
        return
    await call.message.answer(text=command_list, reply_markup=StartKB.as_markup())


'''
Команда для открытия главного меню
'''
@start_router.message(Command("menu"))
async def main_menu(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(text= command_list, reply_markup=StartKB.as_markup())


'''
Обработчик команды /stop
'''
@start_router.message(StateFilter('*'), F.text == '/stop')
@error_handler
async def stop(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(text= command_list, reply_markup=StartKB.as_markup())