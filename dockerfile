FROM python:3.9-alpine

WORKDIR /src

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1 
ENV thread=2
ENV worker=1
ENV ip=0.0.0.0
ENV port=80

COPY ./RateLimit .
RUN pip install --no-cache-dir django redis django-redis gunicorn psycopg2-binary

# production
# CMD  gunicorn --workers=${worker} --threads=${thread} -b ${ip}:${port} RateLimit.wsgi 

# live development
CMD python3 ./manage.py runserver ${ip}:${port} 
