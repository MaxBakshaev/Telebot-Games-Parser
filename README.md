
Образец бота: <https://t.me/LessPriceSteamGames_bot>

# Телеграмм бот Telebot-Games-Parser

### О боте:

Бот находит самые дешевые ключи для Steam региона Россия, а также показывает раздачи бесплатных игр.

---
### Команды:
* __/start__ - начало работы с ботом.
* __/search__ -  найти самые дешевые игры для Steam.
* __/free__ - получить информацию о раздаче бесплатных игр.
* __/help__ - основные возможности бота.

---
### Установка и запуск:

1. Добавьте токен Вашего бота в файл .env. <br/>
Получить токен и создать бота можно по ссылке: <https://t.me/botfather>. <br/>


2. Склонируйте репозиторий и перейдите в рабочую директорию проекта:
```
git clone https://github.com/MaxBakshaev/Telebot-Games-Parser.git
```
```
cd Telebot-Games-Parser
```
3. Создайте и активируйте виртуальную среду:
```
python -m venv venv
```
```
venv\Scripts\activate
```
4. Установите зависимости:
```
pip install -r requirements.txt
```
5. Запуск и остановка бота:
```
python src/main.py
```
```
Ctrl + C
```