# Use an official Python runtime as a parent image
FROM python:3.7

RUN apt-get update

RUN pip install virtualenv

RUN virtualenv /venv -p python3.7

ENV VIRTUAL_ENV /venv
ENV PATH /venv/bin:$PATH

# Copy the application's source code
WORKDIR /src

COPY . /src

COPY requirements.txt /src/

RUN pip install -r /src/requirements.txt

CMD python app/main.py

# Make port 8080 available to the world outside this container
#EXPOSE 8080