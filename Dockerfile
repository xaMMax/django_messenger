FROM python:3.12-slim

RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /django_messenger_project

COPY ./requirements.txt /django_messenger_project/requirements.txt

RUN pip install --no-cache-dir -r /django_messenger_project/requirements.txt

COPY . /django_messenger_project

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]