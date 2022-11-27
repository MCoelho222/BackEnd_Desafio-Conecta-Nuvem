
# FROM python:3.10-alpine
# WORKDIR /app
# # RUN apt-get update -y
# # RUN apt-get install -y python-pip python-dev

# COPY requirements.txt requirements.txt

# RUN pip3 install -r requirements.txt
# COPY . .

# CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]

# Use the official lightweight Python image.
# https://hub.docker.com/_/python
FROM python:3.10-slim

# Allow statements and log messages to immediately appear in the Knative logs
ENV PYTHONUNBUFFERED True

# Copy local code to the container image.
ENV APP_HOME /app
WORKDIR $APP_HOME
COPY ./BackEnd_Desafio-Conecta-Nuvem ./

# Install production dependencies.
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install gunicorn

# Run the web service on container startup. Here we use the gunicorn
# webserver, with one worker process and 8 threads.
# For environments with multiple CPU cores, increase the number of workers
# to be equal to the cores available.
# Timeout is set to 0 to disable the timeouts of the workers to allow Cloud Run to handle instance scaling.
CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 --timeout 0 app:app