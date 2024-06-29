from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton
from aiogram.filters.callback_data import CallbackData
from Auxiliaries import error_handler

'''
Настройка пагинации (все ниже)
Я просто хз как эта хуйня работает это просто копипаста
'''
class Pagination(CallbackData, prefix="pag"):
    action: str  # Действие
    page: int  # Номер страницы

class Pagination2(CallbackData, prefix="page"):
    action: str  # Действие
    page: int  # Номер страницы




async def paginator(themes : list, page: int = 0, ):
    builder = InlineKeyboardBuilder() 

    start_offset = page * 3  # Вычисление начального смещения на основе номера страницы
    limit = 3  # Определение лимита тем на одной странице
    end_offset = start_offset + limit  # Вычисление конечного смещения

    for theme in themes[start_offset:end_offset]:  
        builder.button(text=theme ,callback_data=f"theme_{theme}")  # Добавление кнопки для каждой темы
    buttons_row = []  
    if page > 0:  
        buttons_row.append(InlineKeyboardButton(text="⬅️ Назад", callback_data=Pagination(action="prev", page=page - 1).pack()))  # Добавление кнопки "назад"
    if end_offset < len(themes):  
        buttons_row.append(InlineKeyboardButton(text="Вперед ➡️", callback_data=Pagination(action="next", page=page + 1).pack()))  # Добавление кнопки "вперед"
    
    builder.row(*buttons_row)  
    builder.adjust(1,)
    return builder.as_markup()  



async def paginator_for_themed_learn(themes : list, page: int = 0):
    builder = InlineKeyboardBuilder() 

    start_offset = page * 3  # Вычисление начального смещения на основе номера страницы
    limit = 3  # Определение лимита тем на одной странице
    end_offset = start_offset + limit  # Вычисление конечного смещения

    for theme in themes[start_offset:end_offset]:  
        builder.button(text=theme ,callback_data=f"learn_themed_{theme}")  # Добавление кнопки для каждой темы
    buttons_row = []  
    if page > 0:  
        buttons_row.append(InlineKeyboardButton(text="⬅️ Назад", callback_data=Pagination2(action="prev", page=page - 1).pack()))  # Добавление кнопки "назад"
    if end_offset < len(themes):  
        buttons_row.append(InlineKeyboardButton(text="Вперед ➡️", callback_data=Pagination2(action="next", page=page + 1).pack()))  # Добавление кнопки "вперед"
    
    builder.row(*buttons_row)  
    builder.adjust(1,)
    return builder.as_markup()  

  