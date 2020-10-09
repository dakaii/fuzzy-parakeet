FROM python:3.8-alpine

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apk add --no-cache gcc musl-dev postgresql-dev \
    libressl-dev libffi-dev python3-dev jpeg-dev zlib-dev

RUN mkdir /code
COPY . /code/
WORKDIR /code
RUN pip install -r requirements.txt

CMD gunicorn -b :$PORT core.wsgi