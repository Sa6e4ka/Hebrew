from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from Database.models import User, Competition
from Loggs import logger


'''
Функция для получения id пользователя
'''
async def orm_get_user_id(session: AsyncSession, chat_id) -> str:
    user_query = select(User.user_id).where(User.chat_id == chat_id)
    user_result  = await session.execute(user_query)
    return user_result.scalars().first()


'''
Функция orm_add_user для добавления пользователя в базу данных
'''
async def orm_add_user(session: AsyncSession, username: str, chat_id: str) -> bool: 
# Проверка на наличие пользователя в базе при вводе команды регистарции
    try:
        query = select(User).where(User.chat_id == chat_id)
        result = await session.execute(query)

        if result.scalars().first(): 
            logger.info(f"Пользователь {username} попытался зарегистрироваться повторно") 
            return 
        
    # Добавление нового пользователя в случае его отсутствия в базе
        user = User(
            username = username,
            chat_id = chat_id
        )

        session.add(user)
        await session.commit()

        id = await orm_get_user_id(session=session, chat_id=chat_id)

        user_compete = Competition(
            global_points = 0,
            global_attempts = 0,
            global_percentage = 0,
            user_id = id
        )

        session.add(user_compete)
        await session.commit()

    except Exception as e:
        print(e)
