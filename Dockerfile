FROM python:3.10.12-slim

RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    postgresql-client \
    --no-install-recommends && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* \

WORKDIR /usr/src/app

# install dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt

# copy project
COPY . .
