from aiogram.types import BotCommand

private = [
    BotCommand(command="menu", description="Открыть главное меню"),
    BotCommand(command='saveword',description='Сохранить слово в личный словарь 📚'),
    BotCommand(command='learnwords',description= 'Учить слова из личного словаря'),
    BotCommand(command='words',description= 'Показать список моих слов 📝'),
    BotCommand(command='saveontheme',description= 'Добавить слово в общий словарь 🌍'),
    BotCommand(command='learnthemed',description= 'Учить слова по темам 📖'),
    BotCommand(command="compete", description="Режим соревнований 🏆"),
    BotCommand(command='stop',description= 'Остановить урок или соревнования ✋'),
    BotCommand(command='delete',description= 'Удалить слово из словаря ❌'),
    BotCommand(command='addtheme',description= 'Создать новую тему 📂'),
    BotCommand(command='pealim',description= 'Открыть сайт pealim.com 🌐'),
    BotCommand(command='top',description= 'Посмотреть таблицу лидеров 🥇'),
    BotCommand(command='saverule',description= 'Загрузить правила в личный сборник 🗯'),
    BotCommand(command='getrule',description= 'Посмотреть свои правила 🤓'),
    BotCommand(command="dialog", description="Поговорить на Иврите 🗣")
]
