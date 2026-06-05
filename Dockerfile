FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

RUN mkdir -p /data

ENV DATABASE_PATH=/data/tasks.db

EXPOSE 5000

CMD ["python3", "app.py"]
