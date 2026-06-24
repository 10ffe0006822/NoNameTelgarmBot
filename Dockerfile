FROM python:3.12-slim

RUN pip install aiogram
RUN pip install aiohttp
RUN pip install aiohttp-socks

COPY main.py /app/main.py
COPY db.py /app/db.py
WORKDIR /app

ENV TOKEN=''
ENV PROXY=''


CMD ["python", "main.py"]