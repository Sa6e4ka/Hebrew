from sqlalchemy import select, func, desc, asc
from sqlalchemy.ext.asyncio import AsyncSession
from Database.models import Words, User, ThemedWords, Themes, Competition, Rules
from .user_queries import orm_get_user_id


'''
Функция для получения случайного слова из таблицы пользователя
'''
async def orm_get_rand_personal_word(session: AsyncSession, chat_id : str, word: str) -> list:
# Получение id пользователя
    id = await orm_get_user_id(session=session, chat_id=chat_id)
    if word is not None:
        query = (
            select(Words)
                .where(
                    Words.user_id == id, 
                    Words.word != word
                )
                .order_by(func.random())
                    .limit(1)
        )
    else:
    # Сортировка слов в случайном порядке и выборка одного элемента
        query = (
            select(Words)
                .where(
                    Words.user_id == id
                )
                .order_by(func.random())
                    .limit(1)
        )     
    result = await session.execute(query)
    scl = result.scalars().first()

# возврат списка со словом и его переводом
    return scl.word, scl.translation, scl.transcription


'''
Функция для получения списка слов для пользователя
'''
async def orm_get_all_words(session : AsyncSession, chat_id : str) -> list:

# Получение Id пользователя
    id = await orm_get_user_id(session=session, chat_id=chat_id)

# Получение списка слов
    query_words_list = select(Words.word, Words.translation).where(Words.user_id == id).order_by(Words.word.asc())
    result = await session.execute(query_words_list)

    word_list = {row[0]: row[1] for row in result.fetchall()}

# Получения количества слов в списке пользователя
    query_count_words = select(func.count(Words.word)).where(Words.user_id == id)
    count_result = await session.execute(query_count_words)
    quantity = count_result.scalar_one()

    
    return word_list, quantity


'''
Функция для получения ай ди темы по назанию
'''
async def orm_get_theme_id(session : AsyncSession, theme : str):
    query = select(Themes.theme_id).where(Themes.theme_name == theme).limit(1)

    exc = await session.execute(query)
    return exc.scalars().first()


'''
Функция для получения списка слов по определенной теме
'''
async def orm_get_themed_words_list(session : AsyncSession, theme : dict) -> list:
    # Получение Id пользователя
    id = await orm_get_theme_id(session=session, theme=theme["theme"])

# Получение списка слов
    query_words_list = select(ThemedWords.word, ThemedWords.translation).where(ThemedWords.theme_id == id).order_by(ThemedWords.word.asc())
    result = await session.execute(query_words_list)

    word_list = {row[0]: row[1] for row in result.fetchall()}

# Получения количества слов в списке пользователя
    query_count_words = select(func.count(ThemedWords.word)).where(ThemedWords.theme_id == id)
    count_result = await session.execute(query_count_words)
    quantity = count_result.scalar_one()

    return word_list, quantity


'''
Функция для случайной выборки слова по определенной теме
'''
async def orm_get_random_themed_word(session : AsyncSession, data : dict) -> str:
    id = await orm_get_theme_id(session=session, theme = data["theme"])
    if "word" in data:
        query = (
            select(ThemedWords)
                .where(
                    ThemedWords.theme_id == id, 
                    ThemedWords.word != data["word"]
                )
                .order_by(func.random())\
                    .limit(1)
        )
    else:
        query = select(ThemedWords).where(ThemedWords.theme_id == id).order_by(func.random()).limit(1)
    exc = await session.execute(query)

    result = exc.scalars().first()

    print(result.word)

    return result.word, result.translation, result.transcription


'''
Функция для получения списка тем
'''
async def orm_get_theme_list(session : AsyncSession):
    query = select(Themes.theme_name).order_by(Themes.theme_name.asc())
    result = await session.execute(query)
    result_fetch = result.fetchall()

    themes_list = []
    for i in result_fetch:
        themes_list.append(i[0])

    return themes_list


'''
Функция для получения случайного слова из общей таблицы
'''
async def orm_get_rand_global_word(session: AsyncSession):
    query = select(ThemedWords).order_by(func.random())

    execution = await session.execute(query)
    result = execution.scalars().first()

    return result.word, result.translation, result.transcription


'''
Функция для получения соревновательных данных о пользователе
'''
async def orm_get_user_compete_information(session: AsyncSession, id : str) -> dict:

    query = select(Competition).where(Competition.user_id == id)
    execution = await session.execute(query)
    result = execution.scalars().first()

    point_dict = {
        "points" : result.global_points,
        "attempts" : result.global_attempts,
        "percentage" : round(result.global_percentage, 2) 
    }

    return point_dict


'''
Функция для получения топ пользователей 
'''
async def orm_get_top_users(session: AsyncSession):

    query1 = (
        select(Competition.user_id)
        .order_by(
            desc(Competition.global_points), 
            desc(Competition.global_percentage)
        )
    )

    execution = await session.execute(query1)
    result = execution.scalars().all()
    
    usernames = []

    for i in result:
        query2 = select(User.username).where(User.user_id == i)

        execution2 = await session.execute(query2)
        usernames.append(execution2.scalars().first())
    
    users_points = []

    for i in result:
        query3 = (
        select(
            Competition 
        )
        .where(
            Competition.user_id == i
        )
    )   
        
        execution = await session.execute(query3)
        fine = execution.scalars().first()

        data_list = [
            fine.global_points, 
            fine.global_percentage
        ]
        users_points.append(data_list)

    top_dict = {}

    for i, k in zip(usernames, users_points):
        top_dict[i] = k 
    
    return top_dict


'''
Функция для получения правила по его названию
'''
async def orm_get_rule(session: AsyncSession, data: dict) -> str:
    id = await orm_get_user_id(session=session, chat_id=data["chat_id"])

    query = (
        select(Rules.rule)
            .where(
                Rules.name_rule == data["name_rule"],
                Rules.user_id == id
            )
    )
    execution = await session.execute(query)
    result = execution.scalars().first()
    
    return result


'''
Получения списка названий правил
'''
async def orm_get_name_rules_list(session: AsyncSession, chat_id: str) -> list:
    id = await orm_get_user_id(session=session, chat_id=chat_id)

    query = (
        select(Rules.name_rule)
            .where(
                Rules.user_id == id
            )
                .order_by(asc(Rules.name_rule))
    )
    execution = await session.execute(query)
    result = execution.scalars().all()

    return result