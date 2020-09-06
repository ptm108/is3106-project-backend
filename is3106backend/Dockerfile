# pull official base image
FROM python:3.8.3-alpine

# set working directory
WORKDIR /is3106backend/

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1 
ENV PYTHONUNBUFFERED 1

# install psycopg2 dependencies
RUN apk update \
    && apk add postgresql-dev gcc python3-dev musl-dev

# install dependencies 
COPY ./requirements.txt . 
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# copy entrypoint.sh
COPY ./entrypoint.sh .

# copy project
COPY . .

# run entrypoint.sh
# ENTRYPOINT [ "/is3106backend/entrypoint.sh" ]