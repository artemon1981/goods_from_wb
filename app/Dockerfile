FROM python:3.10

WORKDIR /fastapi

# Скопируйте файл с зависимостями
COPY requirements.txt .
RUN pip install -r requirements.txt --no-cache-dir

# Проверка наличия файлов до копирования
RUN ls -la /fastapi

# Копируем код приложения
COPY ./app /fastapi/app
COPY ./alembic /fastapi/alembic
COPY alembic.ini /fastapi/alembic.ini

# Проверка наличия файлов после копирования
RUN ls -la /fastapi
RUN ls -la /fastapi/app
RUN ls -la /fastapi/alembic

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
