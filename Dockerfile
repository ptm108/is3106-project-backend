# pull official base image
FROM python:3.8.3-alpine

# set working directory
WORKDIR /is3106backend/

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1 
ENV PYTHONUNBUFFERED 1

# install dependencies 
COPY ./requirements.txt . 
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

#copy project
COPY . .
