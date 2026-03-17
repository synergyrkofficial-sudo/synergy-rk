FROM python:3.13-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

COPY . /app

# Render sets $PORT automatically. Default to 5000 for local runs.
ENV PORT=5000

CMD ["sh", "-c", "gunicorn -b 0.0.0.0:${PORT} app:app"]

