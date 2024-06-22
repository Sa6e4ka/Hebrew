from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession
from Database.models import Words, ThemedWords, Rules
from .user_queries import orm_get_user_id


'''
Функция удаления слова
'''
async def orm_delete_word(session : AsyncSession, word, chat_id) -> None:
# Получение id Пользователя
    id = await orm_get_user_id(session=session, chat_id=chat_id)

    query = select(Words.word).where(Words.word == word, Words.user_id == id)
    result = await session.execute(query)

    if result.scalars().first():
    # Запрос удаления слова
        query = delete(Words).where(Words.word == word, Words.user_id == id)
        await session.execute(query)
        await session.commit()
        return
    return "Такого слова в твоем словаре нет 😨"


'''
Функция удаления слова из общей таблицы
'''
async def orm_delete_themed(session: AsyncSession, word: str) -> None:
    query_get = (
        select(ThemedWords.word)
        .where(
            ThemedWords.word == word
        )
    )

    execution = await session.execute(query_get)
    result = execution.scalars().first()
    if result:    
        query_del = (
            delete(ThemedWords)
            .where(
                ThemedWords.word == word
            )
        )

        await session.execute(query_del)
        await session.commit()
        return
    
    raise AttributeError



'''
Функция для удаления правила
'''
async def orm_delete_rule(session: AsyncSession, data: dict) -> None:
    id = await orm_get_user_id(session=session, chat_id=data["chat_id"])
    
    query = (
        delete(Rules)
            .where(
                Rules.name_rule == data["name_rule"],
                Rules.user_id == id
            )
            
    )
    await session.execute(query)
    await session.commit()