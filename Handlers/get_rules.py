from aiogram import F, Router
from aiogram.filters import Command, StateFilter, or_f
from aiogram.fsm.context import FSMContext
from aiogram.types import  Message, CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession
from Database import orm_get_rule, orm_get_name_rules_list

from Auxiliaries import button, error_handler, Pagination3, paginator_for_rules
from typing import Union

# Get Rules Router
get_rules_router = Router()


'''

'''
async def show_rules_func(message_or_call: Union[Message, CallbackQuery], session: AsyncSession):
    names = await orm_get_name_rules_list(session=session, chat_id = message_or_call.chat.id if isinstance(message_or_call, Message) else message_or_call.message.chat.id)
    
    if len(names) == 0:
        text = "Похоже, что ни одного правила еще не было добавлено в твой запас"
        reply_markup = button(["Главное меню", "Добавить правило"]) 
        
        if isinstance(message_or_call, Message):
            await message_or_call.answer(text=text, reply_markup=reply_markup)
            return
        await message_or_call.message.edit_text(text=text, reply_markup=reply_markup)
        return
    
    KB = await paginator_for_rules(page=0, name_rules=names)
    print(KB)
    text = "Выбери тему, по которой хочешь учить слова"
    
    if isinstance(message_or_call, Message):
        await message_or_call.answer(text=text, reply_markup=KB)
        return
    await message_or_call.message.edit_text(text=text, reply_markup=KB)


'''

'''
@get_rules_router.message(Command("getrule"))
@error_handler
async def get_rule_on_command(message: Message, session: AsyncSession):
    await show_rules_func(message_or_call=message, session=session)

    
'''

'''
@get_rules_router.callback_query(or_f(F.data == "Смотреть свои правила", F.data == "Посмотреть другие правила"))
@error_handler
async def get_rule_on_button(call: CallbackQuery, session: AsyncSession):
    await show_rules_func(message_or_call=call, session=session)


'''

'''
@get_rules_router.callback_query(Pagination3.filter())
@error_handler
async def pagination_handler(call: CallbackQuery, callback_data: Pagination3, session: AsyncSession):
    page = callback_data.page  # Получение номера страницы из callback data
    print(page)
    # Функция получения списка тем
    themes = await orm_get_name_rules_list(session=session, chat_id=call.message.chat.id)  

    await call.message.edit_reply_markup(reply_markup=await paginator_for_rules(page=page, themes=themes))  # Обновление клавиатуры при нажатии кнопок "вперед" или "назад"


'''

'''
@get_rules_router.callback_query(F.data.startswith("name_rule_"))
@error_handler
async def show_rule(call: CallbackQuery, state: FSMContext, session: AsyncSession):
    await state.update_data(name_rule = call.data.split("name_rule_")[-1])
    await call.answer()

    rule = await orm_get_rule(
        session=session, 
        data={
            "name_rule": call.data.split("name_rule_")[-1], 
            "chat_id" : call.message.chat.id
        }
    )
    
    await call.message.edit_text(
        text=f"<b>Правило, которое ты хотел получить:</b>\n\n{rule}", 
        reply_markup=button(["Посмотреть другие правила"])
    )