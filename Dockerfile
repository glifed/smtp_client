# Используем базовый образ Python
FROM python:3.10

# Устанавливаем рабочую директорию в контейнере
WORKDIR /app

# Копируем зависимости (файл requirements.txt)
COPY app/requirements.txt .

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Копируем содержимое текущей директории в контейнер
COPY ./app .

# Определяем команду для запуска вашего приложения
CMD ["python", "main.py"]
