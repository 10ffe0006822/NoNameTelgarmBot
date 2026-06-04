FROM python:3.11-slim

RUN pip install aiogram

COPY main.py /app/main.py
WORKDIR /app

ENV TOKEN=''


CMD ["python", "main.py"]