# Volleyball Matches Scraper

Скрапер результатов воллейбольных матчей с [Ресурса](https://volleyballworld.com).

### Стек: 
`docker`, `playwright`, `tor`, `sqlite3`, `asyncio`.

В этом проекте:
- создание docker-образа на основе `Ubuntu:jammy`
- маскировка запросов через сеть `tor`
- создание датасета в виде базы данных `sqlite3` по результатам скрапинга

# Установка (Linux)

На хосте должен быть установлен `docker`.

```bash
cd volleyball-matches-scraper
```

1. Создание контейнера
```bash
docker build -t volleyball-matches-scraper .
```

Параметры сборки можно передать с флагом `--build-arg VAR1=... VAR2=...`

Возможные параметры сборки:
| Параметр | Описание | Значение по-умолчанию |
| :------: | :------- | :-------------------: |
| PROJECT_NAME | Имя проекта. Используется для создания каталогов внутри контейнера | volleyball-matches-scraper |
| GROUP_NAME | Группа пользователя внутри контейнера | vscode |
| USER_NAME | Имя пользователя внутри контейнера | vscode |
| TOR_PASSWORD | Пароль пользователя для доступа в tor внутри контейнера | password |

2. Запуск

```bash
docker run volleyball-matches-scraper
```

Параметры запуска можно передать с флагом `-e ENVVAR1=... ENVVAR2=...`

Возможные параметры запуска:
