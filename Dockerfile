# pull official base image
FROM python:3.12.4-slim

# set working directory
RUN mkdir /backend
WORKDIR /backend

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED=1 \
    VIRTUAL_ENV=/.venv
ENV PATH=$VIRTUAL_ENV/bin:$PATH


# install system dependencies
RUN apt-get update \
  && apt-get -y install gcc libpq-dev \
  && apt-get clean

# install dependencies
RUN python -m venv $VIRTUAL_ENV && pip install --no-cache-dir poetry
COPY pyproject.toml poetry.lock ./
ARG RELEASE=false
RUN ! $RELEASE && poetry install --no-cache --no-root --only dev || $RELEASE
RUN poetry install --no-cache --no-root --only main

# Add health check
HEALTHCHECK --interval=10s CMD python manage.py check

# copy entrypoint.sh and .env
COPY .env /backend
COPY scripts/entrypoint.sh /
RUN sed -i 's/\r$//g'  /entrypoint.sh
RUN chmod +x /entrypoint.sh

# add app
COPY src /backend/

# Set default port and expose it
ARG PORT=8000
ENV PORT=$PORT
EXPOSE $PORT

# run entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]
