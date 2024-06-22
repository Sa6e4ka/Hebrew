from loguru import logger

# Логгеры для дебага и эррора, файлы отправляются по команде /loggs
DEBUG = logger.add("loggs/debug.log", format="--------\n{time:DD-MM-YYYY HH:mm}\n{level}\n{message}\n--------", level='DEBUG', rotation='1 week')

