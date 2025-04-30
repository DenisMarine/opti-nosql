# syntax=docker/dockerfile:1

# Comments are provided throughout this file to help you get started.
# If you need more help, visit the Dockerfile reference guide at
# https://docs.docker.com/go/dockerfile-reference/

# Want to help us make this template better? Share your feedback here: https://forms.gle/ybq9Krt8jtBL3iCk7

ARG PYTHON_VERSION=3.10.12
FROM python:${PYTHON_VERSION}

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./app /code/app

RUN python3 -m venv venv && \
    . venv/bin/activate && \
    python -m pip install --no-cache-dir --no-cache -r "requirements.txt"

# Expose the port that the application listens on.
EXPOSE 8000

COPY ./app /code/app

CMD ["sh", "-c", "python3 app/databases/populate/populate_neo4j.py && uvicorn app.main:app --reload --host 0.0.0.0 --port 8000"]
