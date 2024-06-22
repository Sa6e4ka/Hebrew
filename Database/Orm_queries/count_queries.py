from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from Database.models import ThemedWords


'''
Функция для подсчета слов в общей таблице (нужно для того, чтобы открыть соревновательный режим, когда в таблице будет больше 50 слов)
'''
async def orm_count_all_words(session: AsyncSession):
    query = select(func.count(ThemedWords.word))

    execution = await session.execute(query)
    result = execution.scalar()

    return result