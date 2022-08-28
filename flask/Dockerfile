FROM python:3.7
ENV PYTHONUNBUFFERED=1
RUN python -m pip install flask==2.1.2 flask_restful==0.3.9 requests==2.27.1 pandas==1.3.5 numpy==1.21.6 tensorflow==2.9.1 gunicorn==20.1.0

WORKDIR /app

COPY . /app/