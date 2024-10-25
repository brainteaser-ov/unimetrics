FROM python:3.9-slim

ENV PYTHONUNBUFFERED 1

WORKDIR /code

COPY requirements.txt /code/

RUN pip install --no-cache-dir -r requirements.txt

COPY . /code/

# Собираем статические файлы
# Собираем статические файлы
RUN python manage.py collectstatic --noinput