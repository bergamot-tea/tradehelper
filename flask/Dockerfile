FROM python:3.7
ENV PYTHONUNBUFFERED=1
RUN python -m pip install flask flask_restful requests pandas numpy tensorflow gunicorn

WORKDIR /app

COPY . /app/