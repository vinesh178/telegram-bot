# syntax=docker/dockerfile:1
FROM python:3.10-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

RUN groupadd -r myuser && useradd -r -g myuser myuser

RUN mkdir /app/downloads && chown -R nobody:nogroup /app

RUN chown -R myuser:myuser /app/downloads

USER myuser

EXPOSE 8033

CMD ["python3", "telegram-bot.py"]