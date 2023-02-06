# Проект Yamdb_final
![example workflow](https://github.com/dimabaril/yamdb_final/actions/workflows/yamdb_workflow.yml/badge.svg)
## Проект доступен по адресу:
(vps может быть выключен)
http://51.250.86.197/redoc/ - описание запросов API  
http://51.250.86.197/admin/ - админка  
http://51.250.86.197/api/v1/titles/ - пример для запроса по API  
## Описание.
Проект собирает **отзывы (Review)** пользователей на **произведения (Titles)**. Произведения делятся на категории: "Книги", "Фильмы", "Музыка". Список **категорий (Category)** может быть расширен администратором.
Сами произведения в не хранятся, здесь нельзя посмотреть фильм или послушать музыку.
В каждой категории есть **произведения**: книги, фильмы или музыка. Например, в категории "Книги" могут быть произведения "Винни Пух и все-все-все" и "Марсианские хроники", а в категории "Музыка" — песня "Давеча" группы "Насекомые" и вторая сюита Баха.
Произведению может быть присвоен **жанр** (**Genre**) из списка предустановленных (например, «Сказка», «Рок» или «Артхаус»). Новые жанры может создавать только администратор.
Пользователи оставляют к произведениям текстовые **отзывы** (**Review**) и ставят произведению оценку в диапазоне от одного до десяти (целое число); из пользовательских оценок формируется усреднённая оценка произведения — **рейтинг** (целое число).
## Инструкция по запуску
Для запуска необходимо из корневой папки проекта ввести в консоль(bash или zsh) команду:
```
docker-compose up
```
Затем узнать id контейнера, для этого вводим
```
docker container ls
```
В ответ получаем примерно следующее
```
CONTAINER ID   IMAGE                     COMMAND                  CREATED         STATUS         PORTS                    NAMES
ab8cb8741e4a   nginx:1.19.0              "/docker-entrypoint.…"   7 minutes ago   Up 2 minutes   0.0.0.0:80->80/tcp       dimabaril_nginx_1
f78cc8f246fb   dimabaril/yamdb_final:latest   "/bin/sh -c 'gunicor…"   7 minutes ago   Up 2 minutes   0.0.0.0:8000->8000/tcp   dimabaril_web_1
a68243a0a5e2   postgres:12.4             "docker-entrypoint.s…"   7 minutes ago   Up 2 minutes   5432/tcp                 dimabaril_db_1
```
Нас интересует контейнер dimabaril_web_1, заходим в него командой
```
docker exec -it <CONTAINER ID> bash
```
И делаем миграцию БД, и сбор статики
```
python manage.py migrate
python manage.py collectstatic
```
При желании можно загрузить тестовую бд с контентом
```
python manage.py loaddata fixtures.json
```
## Технологии
- Python 3.7
- Django 2.2.19
- Postgresql
- Nginx
- Docker-compose
- GitHub Actions
## Ресурсы API YaMDb
- Ресурс **auth**: аутентификация.
- Ресурс **users**: пользователи.
- Ресурс **titles**: произведения, к которым пишут отзывы (определённый фильм, книга или песенка).
- Ресурс **categories**: категории (типы) произведений («Фильмы», «Книги», «Музыка»).
- Ресурс **genres**: жанры произведений. Одно произведение может быть привязано к нескольким жанрам.
- Ресурс **reviews**: отзывы на произведения. Отзыв привязан к определённому произведению.
- Ресурс **comments**: комментарии к отзывам. Комментарий привязан к определённому отзыву.
## Пользовательские роли
- **Аноним** — может просматривать описания произведений, читать отзывы и комментарии.
- **Аутентифицированный пользователь (user)** — может читать всё, как и
- **Аноним**, может публиковать отзывы и ставить оценки произведениям (фильмам/книгам/песенкам), может комментировать отзывы; может редактировать и удалять свои отзывы и комментарии, редактировать свои оценки произведений. Эта роль присваивается по умолчанию каждому новому пользователю.
- **Модератор (moderator)** — те же права, что и у **Аутентифицированного пользователя**, плюс право удалять и редактировать **любые** отзывы и комментарии.
- **Администратор (admin)** — полные права на управление всем контентом проекта. Может создавать и удалять произведения, категории и жанры. Может назначать роли пользователям.
- **Суперюзер Django** должен всегда обладать правами администратора, пользователя с правами admin. Даже если изменить пользовательскую роль суперюзера — это не лишит его прав администратора. Суперюзер — всегда администратор, но администратор — не обязательно суперюзер.
## Шаблон наполнения env-файла:
1. Указываем, что работаем с postgresql:
```
DB_ENGINE=django.db.backends.postgresql
```
2. Указываем имя базы данных:
```
DB_NAME=postgres
```
3. Указываем логин для подключения к базе данных:
```
POSTGRES_USER=login
```
4. Указываем пароль для подключения к БД:
```
POSTGRES_PASSWORD=password
```
5. Указываем название сервиса (контейнера):
```
DB_HOST=db
```
6. Указываем порт для подключения к БД:
```
DB_PORT=5432
```
## Автор
- Барилкин Дмитрий
