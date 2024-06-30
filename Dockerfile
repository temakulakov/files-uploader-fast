# Dockerfile
FROM python:3.9

# Установка зависимостей
COPY requirements.txt .
RUN pip install -r requirements.txt

# Копирование приложения
COPY app /app

# Задание рабочей директории
WORKDIR /app

# Команда для запуска приложения
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
