from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command, StateFilter
from aiogram.types import  Message 
from Auxiliaries import button

in_progress_router = Router()

functions_in_progress_list = ["getrule", "dialog"]


@in_progress_router.message(StateFilter("*"), Command(commands=functions_in_progress_list))
async def in_progress_error(message: Message, state: FSMContext):
    await message.answer("<b>Извините, за неудобства</b> 👷🪛\n\nДаннная функция находится в разработке", reply_markup=button(["Главное меню"]))
    await state.clear()