# Импортируем нужные дополнительные модули
import os
import asyncio
from Loggs import logger

# Импортируем нужные модули из aiogram
from aiogram import Bot, Dispatcher, F
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command
from aiogram.types import BotCommandScopeAllPrivateChats, Message
from aiogram.client.default import DefaultBotProperties

# Достаем токен бота и url базы данных из переменной окружения
from dotenv import find_dotenv, load_dotenv
load_dotenv(find_dotenv())

# Импортируем функции создания базы данных и сессию
try:
    from Database import create_db, session_maker
except Exception as e:
    logger.error(f'Ошибка в запросе к sql: {e}')

# Из папки handlers импортируем все хендлеры
from Handlers import (
    start_router, words_router, learn_router, 
    save_personal_router, save_general_router, 
    delete_router, compete_router, global_learn_router, logging_router
)

# Импортируем команды
from Auxiliaries.commands import private

# Создаем объект бота (передаем ему режим парсига получаемых ответов)
bot = Bot(token=os.environ.get("TOKEN"), default=DefaultBotProperties(parse_mode='HTML'))
# Создаем объект диспетчера
dp = Dispatcher()

# Добавляем Middlewares 
from Middleware import DataBaseSession

# Подключаем к диспетчеру все роутеры из создаваемых хендлеров
dp.include_routers(start_router, save_personal_router, words_router, delete_router, compete_router, learn_router, global_learn_router, logging_router, save_general_router)

# Добавляем основные "глобальные" хендлеры
@dp.message(Command('state'))
async def state_get(message: Message, state: FSMContext):
    current_state = await state.get_state()
    await message.answer(text=f'Текущее состояние: {current_state}')

@dp.message(Command('stateclear'))
async def clear_state(message: Message, state: FSMContext):
    current_state = await state.get_state()
    await state.clear()
    clear_state = await state.get_state()
    await message.answer(f'Состояние <b>{current_state}</b> сменилось на <b>{clear_state}</b>')

# Запускаем бота, помещаем доступные апдейты в start_polling
# отключаем обработку незавершившихся запросов
# Подключаем базу данных
async def main():
    dp.update.middleware(DataBaseSession(session_pool=session_maker))
    await create_db()
    await bot.delete_webhook(drop_pending_updates=True)
    await bot.set_my_commands(commands=private, scope=BotCommandScopeAllPrivateChats())
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())

# Запуск main
if __name__ == "__main__":
    try:
        logger.info("I'M ALIVE")
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info('Бот остановлен!')
        pass
    except Exception as e:
        logger.error(f'CRITICAL ERROR: {e}')
