# Use a Python image
FROM python:3.9-slim

WORKDIR /app
# задаются значения переменных окружения
ENV PYTHONDONTWRITEBYTECODE 1
# чтобы Python не создавал скомпилированные файлы для ускорения запуска
ENV PYTHONUNBUFFERED 1
# чтобы Python не использовал буферизацию ввода-вывода

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . /app
