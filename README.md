# Код Петербурга


## Город Талантов


### Миграции базы данных 

Управление версиями БД осуществляется с помощью пакета `alembic`.

#### Создание миграции

Для автоматического создания миграции выполните
```shell
alembic revision --autogenerate -m "Name of migration"
```

если проект запущен локально.

И если запущен через docker compose

```shell
docker-compose exec backend alembic revision --autogenerate -m "Name of migration"
```

#### Применение миграции

Для обновления/инициализации таблиц через миграции выполните команду

```shell
alembic upgrade head
```

или для docker compose

```shell
docker-compose exec backend alembic upgrade head
```