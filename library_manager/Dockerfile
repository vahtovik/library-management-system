FROM python:3.11-alpine

WORKDIR /app
COPY . /app/

RUN pip install -r requirements.txt

CMD python manage.py migrate \
    && python manage.py collectstatic --noinput \
    && gunicorn library_manager.wsgi:application --bind 0.0.0.0:8000
