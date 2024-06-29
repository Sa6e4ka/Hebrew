# Hebrew Learning Bot

Этот проект представляет собой Telegram-бота для изучения иврита русскоговорящей аудиторией. Бот предоставляет различные функции для изучения новых слов, повторения выученных, участия в соревнованиях и управления базой данных.


## Установка и запуск

### Требования

- Python 3.8 или выше
- Виртуальное окружение (рекомендуется)

### Установка

1. Склонируйте репозиторий:
    ```bash
    git clone https://github.com/Sa6e4ka/Hebrew-Bot.git
    ```

2. Перейдите в директорию проекта:
    ```bash
    cd Hebrew-Bot
    ```

3. Создайте и активируйте виртуальное окружение:
    ```bash
    python -m venv venv
    source venv/bin/activate  # На Windows: venv\Scripts\activate
    ```

4. Установите зависимости:
    ```bash
    pip install -r requirements.txt
    ```

5. Создайте файл `.env` в корневой директории проекта и добавьте следующие переменные:
    ```env
    TOKEN=<ваш_токен_бота>
    DATABASE_URL=<ваш_url_базы_данных>
    ```

6. Если запуск бота происходит на Linux Ubuntu 22.04, то необходимо установить пакеты pkg-config и libmysqlclient-dev:
    ```bash
    sudo apt-get update
    sudo apt-get install pkg-config libmysqlclient-dev
    ```

### Запуск

Для запуска бота выполните следующую команду:
```bash
python main.py
