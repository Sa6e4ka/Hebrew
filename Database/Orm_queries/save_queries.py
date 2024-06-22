from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from Database.models import Words, ThemedWords, Themes, Rules
from .user_queries import orm_get_user_id


'''
Функция сохранения слов в личный словарь пользователей
'''
async def orm_save_word(data : dict, session : AsyncSession) -> None:
# Получение id пользователя 
    id = await orm_get_user_id(session=session, chat_id=data["chat_id"])

# Запрос на выборку слова из таблицы
    querry = select(Words.word).where(Words.word == data['word'], Words.user_id == id).limit(1)
    result = await session.execute(querry)

# Проверка наличия слова в таблице
    if result.scalars().first():

    # Если слово в таблице имеется, то обновляем данные о нем (само слово и перевод)
        update_query = update(Words).where(Words.word == data['word']).values(translation = data['translation'])
    
        await session.execute(update_query)
        await session.commit()
        return
    
# Сохраняем новое слово, его перевод и юзера в таблицу
    objects = Words(
        word = data['word'],
        translation = data['translation'],
        transcription = data["transcription"],
        user_id = id
    )

    session.add(objects)
    await session.commit()


'''
Функция для сохранения слов по определенной теме
'''
async def orm_save_themed_word(session : AsyncSession, data : dict) -> None:

    query = select(Themes.theme_id).where(Themes.theme_name == data["theme"])
    result = await session.execute(query)

    id = result.scalars().first()

    word = ThemedWords(
        word = data["word"],
        translation = data["translation"],
        transcription = data["transcription"],
        theme_id = id
    )
    session.add(word)
    await session.commit()


'''
Функция для добавления новой темы
'''
async def orm_save_theme(session : AsyncSession, theme_name : str) -> None:
    theme = Themes(
        theme_name = theme_name
    )

    session.add(theme)
    await session.commit()


'''
функция для загрузки нового правила или обновления старой, если оно уже есть в таблице
'''
async def orm_add_rule(session: AsyncSession, data: dict) -> None:
    id = await orm_get_user_id(session=session, chat_id=data["chat_id"])

    query = (
        select(Rules)
            .where(
                Rules.name_rule == data["name_rule"], 
                Rules.user_id == id
            )
            .limit(1)
    )
    execution = await session.execute(query)
    result = execution.scalars().first()

    if result:
        update_query = (
            update(Rules)
                .where(
                    Rules.user_id == id,
                    Rules.name_rule == data["name_rule"]
                )
                .values(
                    rule = data["rule"]
                )
        )
        await session.execute(update_query) 
        await session.commit()
        return
    
    new_rule =  Rules(
        user_id = id,
        name_rule = data["name_rule"],
        rule = data["rule"]
    )

    session.add(new_rule)
    await session.commit()