'''
Сохранение правил.
Правила добавляет сам пользователь и их может видеть (получать) только он сам.
'''
from asyncio import sleep

from aiogram import F, Router
from aiogram.filters import Command, StateFilter, or_f
from aiogram.fsm.context import FSMContext
from aiogram.types import  Message, CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession
from Database import orm_add_rule, orm_get_rule, orm_get_name_rules_list

from Auxiliaries import button, error_handler, Rule, Pagination3, paginator_for_rules
from typing import Union

# Save Rulw Router
save_rules_router = Router()

'''

'''
async def save_rule(state: FSMContext, message_or_call) -> None:
    message_text = "Введи название правила, которое хочешь сохранить"
    await state.set_state(Rule.first)

    if isinstance(message_or_call, Message):
        await message_or_call.answer(message_text, reply_markup=button(["Отмена"]))
    elif isinstance(message_or_call, CallbackQuery):
        await message_or_call.answer()
        await message_or_call.message.edit_text(message_text, reply_markup= button(["Отмена"]))


'''

'''
@save_rules_router.message(Command("saverule"))
@error_handler
async def saverule_on_command(message: Message, state: FSMContext):
    await save_rule(state=state, message_or_call=message)


'''

'''
@save_rules_router.callback_query(or_f(F.data =="Добавить правило", F.data == "Добавить еще правило", F.data == "Редактировать правило"))
@error_handler
async def saverule_on_button(call: CallbackQuery, state: FSMContext):
    await save_rule(state=state, message_or_call=call)



'''
'''
@save_rules_router.message(F.text, StateFilter(Rule.first))
@error_handler
async def saverule_on_command_2(message: Message, state: FSMContext):
    await state.update_data(name_rule = message.text.lower())
    await message.answer(text="Теперь введи правило")
    await state.set_state(Rule.second)


'''

'''
@save_rules_router.message(F.text, StateFilter(Rule.second))
@error_handler
async def saverule_on_command_3(message: Message, state: FSMContext, session: AsyncSession):
    if not message.text:
        await message.answer("Извини, но пока что сохранять правила можно толко в текстовом виде\n\nЕсли ты видишь необходимость в добавлении возможности сохранения правил картинками или в другом виде, то напиши об этои @megagigapoopfart")
        return
    
    await state.update_data(rule = message.text.lower(), chat_id= message.chat.id)
    state_data = await state.get_data()
    await orm_add_rule(session=session, data=state_data)
    await message.answer("Правило успешно сохранено!\n\nТеперь ты можешь посмотреть список своих правил по команде /rules или нажав на кнопку ниже", reply_markup=button(["Главное меню"]))
    print(state_data)
    await state.clear()





