FROM python:3.12-slim

LABEL authors="reloia"

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip install --no-cache-dir --upgrade -r requirements.txt
RUN pip install --no-cache-dir gunicorn

COPY . /app

RUN rm requirements.txt Dockerfile docker-compose.yml

EXPOSE 8104

CMD ["gunicorn", "main:app", "--workers", "4", "--worker-class", "uvicorn.workers.UvicornWorker", "--bind", "0.0.0.0:8104", "--reload"]