# Проект по размещению объявлений.
### Описание проекта: Пользователь может создавать объявления, получать список объявлений, удалить объявление.
### Также может создать комментарий объявлению и жалобу. Прочитать и удалить жалобы может только администратор. Есть обычный пользователь и администратор, у администратора выданы права суперпользователя.
### Подключена аутентификация с помощью JWT-токена и передачи этого токена в заголовке. Подключено логирование. Подключена база данных Postgres. Приложение запускается через Docker.
### Имеется пагинация, сортировка и фильтрация.
## Технологии которые используются в проекте:
- FastAPI 0.98.0
- Postgres 13.2
- Python 3.9
- Docker
- loguru 0.7.0
- SQLAlchemy 2.0.17
- alembic 1.11.1
- uvicorn 0.22.0

Чтобы запусить проект можно выполнить команду `docker-compose up --build` из директории с файлом docker-compose.yml <br>
Но перед этим надо создать файл .env можно создать в той же директории, что и docker-compose, если хотите в другой директории то придется указать путь к нему в docker-compose, файл имеет такие параметры: <br>
POSTGRES_DB = имя базы данных (можете написать, что угодно) <br>
POSTGRES_USER = имя пользователя базы данных (можете написать, что угодно) <br>
POSTGRES_PASSWORD = пароль базы данных (можете написать, что угодно) <br>
DB_HOST = хост базы данных, надо указать название вашего сервиса в docker-compose.yml если запускаетет через Docker<br>
DB_PORT = порт базы данных (можете написать любой порт, главное чтобы он совпадал с тем, что написано в docker-compose) <br>
SECRET = секрктный ключ, можно написать любую рандомную строку <br>

Посkе команды должны создаться два контейнера с приложением и дазой данных. <br>
По фдресу http://127.0.0.1:8000/docs будет доступна документация к проекту. <br>
Администратор может блокировать пользователей делая patch запрос на http://127.0.0.1:8000/users/<id_пользователя> <br>
и передать в телезапроса параметр {is_active: false} <br>
![Снимок экрана (30)](https://github.com/vomerf/nsk-ad/assets/101176519/56cb5249-8724-454e-8341-5254724f2033)
Примеры запросов на создвание и получение объявлений:
Чтобы создать объявление нужно отправить post запрос на http://127.0.0.1:8000/create-ad и передать два параметра в теле запроса<br>
это текст самого объявления и к какой категории бдует относится данное объявление.<br>
![пример создания объявления](https://github.com/vomerf/nsk-ad/assets/101176519/5e0577a8-5da7-4b45-81e9-e1409a9bad8c)

Чтобы получить объявления нужно выполнить get запрос http://127.0.0.1:8000/list-ad<br>
Получим по умолчанию 10 записей, если нужно меньше или больше то нужно передавать query параметры skip и limit.<br>
Если нужна сортировка то gtthlftncz  
