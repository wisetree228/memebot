[//]: # (# Микелянджело дай пивчик | Mikelanjelo give me beer)

[//]: # ()
[//]: # ([Русская версия]&#40;#russian-version&#41; | [English version]&#40;#english-version&#41;)

[//]: # ()
[//]: # (<a id="russian-version"></a>)

[//]: # (## Русская версия)

[//]: # ()
[//]: # (Идея проекта - попытаться повторить бот для знакомств "Леонардо дай винчик". Реализован весь основной функционал:)

[//]: # (- Создание анкеты &#40;прикрепление медиафайлов работает&#41;)

[//]: # (- Листание подходящих по возрасту и полу анкет &#40;человек сам указывает, какой пол его интересует, максимальная разница в возрасте с показываемыми анкетами 2 года&#41;)

[//]: # (- Редактирование анкеты)

[//]: # (- Лайки на анкеты)

[//]: # (- Просмотр входящих лайков, при взаимном лайке выдаётся ссылка на профиль человека, который тебя лайкнул)

[//]: # (- Реализована настройка местоположения &#40;города и опционально координаты&#41;. При поиске анкеты проверяется либо жительство в одном городе, либо расстояние между пользователями меньше 5км)

[//]: # ()
[//]: # (## Инструкция по локальному запуску)

[//]: # ()
[//]: # (### Предусмотрено 2 варианта запуска:)

[//]: # (1&#41; Через docker-compose с СУБД PostgreSQL и Alembic для управления миграциями &#40;рекомендуется для мощных серверов при большой нагрузке&#41;)

[//]: # (2&#41; Без докера, просто программа python и СУБД sqlite)

[//]: # ()
[//]: # (### Запуск через докер:)

[//]: # (1&#41; В корневой директории проекта создать файл .env и там установить настройки подключения к БД, а также токен вашего телеграмм бота, пример:)

[//]: # (```)

[//]: # (TOKEN=<your_token>)

[//]: # (POSTGRES_USER=wisetree)

[//]: # (POSTGRES_PASSWORD=123456789)

[//]: # (POSTGRES_DB=mydb)

[//]: # (DATABASE_URL=postgresql+asyncpg://wisetree:123456789@db:5432/mydb)

[//]: # (```)

[//]: # (2&#41; Поднять докер &#40;на Windows просто запустите Docker Desktop, на Linux выполните команду `sudo systemctl start docker`&#41;)

[//]: # (3&#41; Когда Docker поднимется, откройте второй терминал и выполните)

[//]: # (```commandline)

[//]: # (sudo docker compose run --rm app alembic revision --autogenerate -m "New migration")

[//]: # (```)

[//]: # (а потом)

[//]: # (```commandline)

[//]: # (sudo docker compose run --rm app alembic upgrade head)

[//]: # (```)

[//]: # (&#40;создание таблиц в БД&#41;)

[//]: # ()
[//]: # (4&#41; Готово, бот должен работать!)

[//]: # ()
[//]: # (### Запуск через питон с sqlite:)

[//]: # (1&#41; Убедитесь, что на устройстве, на котором запускаете, установлен Python.)

[//]: # (2&#41; Создайте виртуальное окружение:)

[//]: # (- для Windows:)

[//]: # (```commandline)

[//]: # (py -m venv venv)

[//]: # (```)

[//]: # (- для Linux:)

[//]: # (```commandline)

[//]: # (python3 -m venv venv)

[//]: # (```)

[//]: # (3&#41; Активируйте:)

[//]: # (- для Windows:)

[//]: # (```commandline)

[//]: # (venv\Scripts\activate)

[//]: # (```)

[//]: # (- для Linux:)

[//]: # (```commandline)

[//]: # (source venv/bin/activate)

[//]: # (```)

[//]: # (4&#41; Установите все зависимости &#40;```pip install -r requirements.txt```&#41;)

[//]: # (5&#41; В корневой директории проекта создайте файл .env и там установите URL для подключения к базе данных и токен бота, пример:)

[//]: # (```)

[//]: # (TOKEN=<your_token>)

[//]: # (DATABASE_URL=sqlite+aiosqlite:///C:/path/to/base/database.db)

[//]: # (```)

[//]: # (Важно: путь до файла бд в URL должен быть абсолютным, а не относительным!)

[//]: # (&#40;Иначе на windows не работают миграции&#41;)

[//]: # ()
[//]: # (6&#41; Перейдите в директорию db &#40;```cd db```&#41; и выполните )

[//]: # (```commandline)

[//]: # (python3 create_all_without_alembic.py)

[//]: # (```)

[//]: # (&#40;создание таблиц в БД&#41;)

[//]: # ()
[//]: # (7&#41; Запустите скрипт, в корневой директории проекта выполните )

[//]: # (```commandline)

[//]: # (python3 main.py)

[//]: # (```)

[//]: # (8&#41; Готово, бот должен работать!)

[//]: # ()
[//]: # (## Генерация документации)

[//]: # (1&#41; Перейдите в папку docs &#40;```cd docs```&#41;)

[//]: # (2&#41; выполните команду )

[//]: # (```commandline)

[//]: # (make html)

[//]: # (```)

[//]: # (&#40;если не сработало, то ```.\make html```&#41;)

[//]: # ()
[//]: # (3&#41; Теперь, когда документация сгенерирована, откройте в браузере файл, который располагается по адресу docs/build/html/index.html)

[//]: # ()
[//]: # (---)

[//]: # (<a id="english-version"></a>)

[//]: # (## English Version)

[//]: # ()
[//]: # (The idea of the project is to try to replicate the dating bot "Leonardo give me wine". All the main functionality has been implemented:)

[//]: # (- Creating a profile &#40;attaching media files works&#41;)

[//]: # (- Browsing suitable profiles based on age and gender &#40;the user specifies the gender they are interested in, with a maximum age difference of 2 years with the displayed profiles&#41;)

[//]: # (- Editing the profile)

[//]: # (- Liking profiles)

[//]: # (- Viewing incoming likes, when a mutual like occurs, a link to the profile of the person who liked you is provided)

[//]: # (- Location settings have been implemented &#40;cities and optionally coordinates&#41;. When searching for a profile, it checks either residence in the same city or the distance between users is less than 5 km)

[//]: # ()
[//]: # (## Instructions for local launch)

[//]: # ()
[//]: # (### There are 2 ways to launch:)

[//]: # (1&#41; Through docker-compose with PostgreSQL and Alembic for migration management &#40;recommended for powerful servers under heavy load&#41;)

[//]: # (2&#41; Without Docker, just the Python program and SQLite database)

[//]: # ()
[//]: # (### Launching via Docker:)

[//]: # (1&#41; In the root directory of the project, create a `.env` file and set the database connection settings as well as your Telegram bot token, example:)

[//]: # (```)

[//]: # (TOKEN=<your_token>)

[//]: # (POSTGRES_USER=wisetree)

[//]: # (POSTGRES_PASSWORD=123456789)

[//]: # (POSTGRES_DB=mydb)

[//]: # (DATABASE_URL=postgresql+asyncpg://wisetree:123456789@db:5432/mydb)

[//]: # (```)

[//]: # (2&#41; Start Docker &#40;on Windows just run Docker Desktop, on Linux run the command `sudo systemctl start docker`&#41;)

[//]: # (3&#41; When Docker is up, open a second terminal and run:)

[//]: # (```commandline)

[//]: # (sudo docker compose run --rm app alembic revision --autogenerate -m "New migration")

[//]: # (```)

[//]: # (then run:)

[//]: # (```commandline)

[//]: # (sudo docker compose run --rm app alembic upgrade head)

[//]: # (```)

[//]: # (&#40;creating tables in the database&#41;)

[//]: # ()
[//]: # (4&#41; Done, the bot should work!)

[//]: # ()
[//]: # (### Launching via Python with SQLite:)

[//]: # (1&#41; Make sure that Python is installed on the device you are running.)

[//]: # (2&#41; Create a virtual environment:)

[//]: # (- for Windows:)

[//]: # (```commandline)

[//]: # (py -m venv venv)

[//]: # (```)

[//]: # (- for Linux:)

[//]: # (```commandline)

[//]: # (python3 -m venv venv)

[//]: # (```)

[//]: # (3&#41; Activate:)

[//]: # (- for Windows:)

[//]: # (```commandline)

[//]: # (venv\Scripts\activate)

[//]: # (```)

[//]: # (- for Linux:)

[//]: # (```commandline)

[//]: # (source venv/bin/activate)

[//]: # (```)

[//]: # (4&#41; Install all dependencies &#40;```pip install -r requirements.txt```&#41;)

[//]: # (5&#41; In the root directory of the project, create a `.env` file and set the URL for connecting to the database and the bot token, example:)

[//]: # (```)

[//]: # (TOKEN=<your_token>)

[//]: # (DATABASE_URL=sqlite+aiosqlite:///C:/path/to/base/database.db)

[//]: # (```)

[//]: # (Important: the path to the database file in the URL must be absolute, not relative!)

[//]: # (&#40;Else, migrations doesn't work on windows&#41;)

[//]: # ()
[//]: # (6&#41; Navigate to the db directory &#40;```cd db```&#41; and run:)

[//]: # (```commandline)

[//]: # (python3 create_all_without_alembic.py)

[//]: # (```)

[//]: # (&#40;creating tables in the database&#41;)

[//]: # ()
[//]: # (7&#41; Run the script, in the root directory of the project run:)

[//]: # (```commandline)

[//]: # (python3 main.py)

[//]: # (```)

[//]: # (8&#41; Done, the bot should work!)

[//]: # ()
[//]: # (## Generating Documentation)

[//]: # (1&#41; Navigate to the docs folder &#40;```cd docs```&#41;)

[//]: # (2&#41; Run the command:)

[//]: # (```commandline)

[//]: # (make html)

[//]: # (```)

[//]: # (&#40;if it doesn't work, then ```.\make html```&#41;)

[//]: # ()
[//]: # (3&#41; Now, when the documentation is generated, open the file located at docs/build/html/index.html in your browser.)