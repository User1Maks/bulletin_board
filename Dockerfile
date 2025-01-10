FROM python:3.12 AS builder
RUN curl -sSL https://install.python-poetry.org | python -
WORKDIR /app
ENV PATH="/root/.local/bin:${PATH}"
ENV PYTHONPATH="/app"
ENV POETRY_VIRTUALENVS_CREATE=false
COPY pyproject.toml poetry.lock ./
RUN poetry install --no-root
RUN poetry remove python-dotenv
RUN poetry add python-dotenv
