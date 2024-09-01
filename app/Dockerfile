FROM python:3.10

WORKDIR /fastapi

# Скопировать файл с зависимостями в рабочую директорию
COPY requirements.txt /fastapi/

# Установить зависимости из файла
RUN pip install -r /fastapi/requirements.txt --no-cache-dir

# Копируем код приложения
COPY ./app /fastapi/app
COPY . .

CMD alembic upgrade head && uvicorn app.main:app --host 0.0.0.0 --port 8000
