# Тестовое задание "Создание REST API приложения"
* Схема базы данных
     ![alt text](imageforreadme/dbSchema.png)
![GitHub top language](https://img.shields.io/github/languages/top/Mike0001-droid/TestFastAPI)

## Установка
1. Клонирование репозитория 

```git clone https://github.com/Mike0001-droid/TestFastAPI.git```

2. Создание виртуального окружения

```python -m venv venv```

3. Активация виртуального окружения

```cd venv/scripts/activate```

4. Установка poetry

```pip install poetry```

5. Установка зависимостей

```poetry install```

6. Заполните файл .env

7. Создание миграции

``` alembic revision --autogenerate -m "название миграции"```

8. Запуск миграции

```alembic upgrade head```

9. Запуск сервера

```uvicorn main:app --reload```
