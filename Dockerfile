# Используйте официальный образ Python как базовый образ
FROM python:3.11-slim

# Установите рабочий каталог
WORKDIR /app

# Скопируйте файлы проекта в рабочий каталог
COPY . /app

# Установите зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Откройте порт для доступа к приложению
EXPOSE 8000

# Команда для запуска приложения
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
