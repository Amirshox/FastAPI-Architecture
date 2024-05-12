# Dockerfile

# pull the official docker image
FROM python:3.11

# set work directory
WORKDIR /app

# copy project
COPY . .

# install dependencies
RUN pip install -r requirements.txt
