from sqlalchemy import select, update, delete, func, desc, asc
from sqlalchemy.ext.asyncio import AsyncSession
from Database.models import Rules
from .user_queries import orm_get_user_id
from Loggs import logger

'''
Структура таблицы Rules:
___________________
| id INT PK       | 
| name_rule STRING|
| rule TEXT       |
| user_id INT FK  |
|_________________|

'''










