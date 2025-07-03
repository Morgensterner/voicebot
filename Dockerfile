FROM python:3.10-slim

# Установка ffmpeg
RUN apt-get update && apt-get install -y ffmpeg

# Установка зависимостей
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем код
COPY . .

# Запускаем бота
CMD ["python", "main.py"]
