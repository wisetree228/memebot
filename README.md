# Мембот | Memebot


[Русская версия](#russian-version) | [English version](#english-version)


<a id="russian-version"></a>

## Русская версия


Бот, в котором можно выкладывать мемы (фото и видео, опционально с подписью). Мемы проходят модерацию у админов и либо одобряются, либо не одобряются,
можно листать выложенные мемы и лайкать их


## Инструкция по локальному запуску


### Предусмотрено 2 варианта запуска:

1) Через docker-compose с СУБД PostgreSQL и Alembic для управления миграциями (рекомендуется для мощных серверов при большой нагрузке)

2) Без докера, просто программа python и СУБД sqlite


### Запуск через докер:

1) В корневой директории проекта создать файл .env и там установить настройки подключения к БД, токен вашего телеграмм бота, а также перечисленные через запятую(без пробелов)
id телеграм аккаунтов, которые будут админами, пример:

```
TOKEN=<your_token>
POSTGRES_USER=wisetree
POSTGRES_PASSWORD=123456789
POSTGRES_DB=mydb
DATABASE_URL=postgresql+asyncpg://wisetree:123456789@db:5432/mydb
ADMINS_ID=12345,65748,838299
```

2) Поднять докер (на Windows просто запустите Docker Desktop, на Linux выполните команду `sudo systemctl start docker`)

3) Когда Docker поднимется, откройте второй терминал и выполните

```commandline
sudo docker compose run --rm app alembic revision --autogenerate -m "New migration"
```

а потом

```commandline
sudo docker compose run --rm app alembic upgrade head
```

(создание таблиц в БД)


4) Готово, бот должен работать!


### Запуск через питон с sqlite:

1) Убедитесь, что на устройстве, на котором запускаете, установлен Python.

2) Создайте виртуальное окружение:

- для Windows:

```commandline
py -m venv venv
```

- для Linux:

```commandline
python3 -m venv venv
```

3) Активируйте:

- для Windows:

```commandline
venv\Scripts\activate
```

- для Linux:

```commandline
source venv/bin/activate
```

4) Установите все зависимости (```pip install -r requirements.txt```)

5) В корневой директории проекта создайте файл .env и там установите URL для подключения к базе данных, id
администраторов(id телеграм аккаунтов через запятую без пробелов) и токен бота, пример:

```
TOKEN=<your_token>
DATABASE_URL=sqlite+aiosqlite:///C:/path/to/base/database.db
ADMINS_ID=12345,65748,838299
```

Важно: путь до файла бд в URL должен быть абсолютным, а не относительным!

(Иначе на windows не работают миграции)


6) Перейдите в директорию db (```cd db```) и выполните 

```commandline
python3 create_all_without_alembic.py
```

(создание таблиц в БД)


7) Запустите скрипт, в корневой директории проекта выполните 

```commandline
python3 main.py
```

8) Готово, бот должен работать!


## Генерация документации

1) Перейдите в папку docs (```cd docs```)

2) выполните команду 

```commandline
make html
```

(если не сработало, то ```.\make html```)


3) Теперь, когда документация сгенерирована, откройте в браузере файл, который располагается по адресу docs/build/html/index.html


---

<a id="english-version"></a>

## English Version

A bot where you can post memes (photos and videos, optionally with captions). Memes are moderated by the admins and either approved or disapproved,
you can scroll through the posted memes and like them.

## Instructions for local launch


### There are 2 ways to launch:

1) Through docker-compose with PostgreSQL and Alembic for migration management (recommended for powerful servers under heavy load)

2) Without Docker, just the Python program and SQLite database


### Launching via Docker:

1) In the root directory of the project, create a `.env` file and set the database connection settings as well as your Telegram bot token.
Also set id of telegram accounts who will be admins in your bot(separated by commas without spaces), example:

```
TOKEN=<your_token>
POSTGRES_USER=wisetree
POSTGRES_PASSWORD=123456789
POSTGRES_DB=mydb
DATABASE_URL=postgresql+asyncpg://wisetree:123456789@db:5432/mydb
ADMINS_ID=12345,65748,838299
```

2) Start Docker (on Windows just run Docker Desktop, on Linux run the command `sudo systemctl start docker`)

3) When Docker is up, open a second terminal and run:

```commandline
sudo docker compose run --rm app alembic revision --autogenerate -m "New migration"
```

then run:

```commandline
sudo docker compose run --rm app alembic upgrade head
```

(creating tables in the database)


4) Done, the bot should work!


### Launching via Python with SQLite:

1) Make sure that Python is installed on the device you are running.

2) Create a virtual environment:

- for Windows:

```commandline
py -m venv venv
```

- for Linux:

```commandline
python3 -m venv venv
```

3) Activate:

- for Windows:

```commandline
venv\Scripts\activate
```

- for Linux:

```commandline
source venv/bin/activate
```

4) Install all dependencies (```pip install -r requirements.txt```)

5) In the root directory of the project, create a `.env` file and set the URL for connecting to the database and the bot token.
Also set id of telegram accounts who will be admins in your bot(separated by commas without spaces), example:

```
TOKEN=<your_token>
DATABASE_URL=sqlite+aiosqlite:///C:/path/to/base/database.db
ADMINS_ID=12345,65748,838299
```

Important: the path to the database file in the URL must be absolute, not relative!

(Else, migrations doesn't work on windows)


6) Navigate to the db directory (```cd db```) and run:

```commandline
python3 create_all_without_alembic.py
```

(creating tables in the database)


7) Run the script, in the root directory of the project run:

```commandline
python3 main.py
```

8) Done, the bot should work!


## Generating Documentation

1) Navigate to the docs folder (```cd docs```)

2) Run the command:

```commandline
make html
```

(if it doesn't work, then ```.\make html```)


3) Now, when the documentation is generated, open the file located at docs/build/html/index.html in your browser.