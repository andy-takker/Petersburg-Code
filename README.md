# Код Петербурга


## Город Талантов




### Миграции БД (Alembic)

Управление версиями БД осуществляется с помощью пакета `alembic`.

#### Создани миграции 

Для автоматического создании миграции при изменении модели данных нужно выполнить:

```shell
alembic revision --autogenerate -m "Name of migration"
```
или при запуске через Docker Compose

```shell
docker-compose exec backend alembic revision --autogenerate -m "Name of migration"
```

#### Применение миграций

Для обновления/инициализации таблиц через миграции выполните

```shell
alembic upgrade head
```
для Docker Compose

```
docker-compose exec backend alembic upgrade head
```
