# syntax=docker/dockerfile:1
FROM python:3.10
# рабочая директория внутри проекта
WORKDIR /app_root

# переменные окружения для python
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# устанавливаем зависимости
RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt

# копируем содержимое текущей папки в контейнер
COPY . .

# запускаем скрипт
CMD ["python", "./kanalservis/__main__.py"]
