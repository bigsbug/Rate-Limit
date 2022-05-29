FROM python:3.9-alpine


WORKDIR /src

ENV thread=2
ENV worker=1
ENV ip=0.0.0.0
ENV port=80

COPY ./RateLimit .
RUN pip install --no-cache-dir django redis django-redis gunicorn psycopg2
CMD  gunicorn --workers=${worker} --threads=${thread} -b ${ip}:${port} RateLimit.wsgi 
