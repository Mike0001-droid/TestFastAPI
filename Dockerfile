FROM python:3.12-slim-bullseye AS builder

WORKDIR /app
COPY poetry.lock pyproject.toml ./

RUN python -m pip install --no-cache-dir poetry==1.4.2 \
    && poetry config virtualenvs.in-project true \
    && poetry install --without dev,test --no-interaction --no-ansi

FROM python:3.12-slim-bullseye

COPY . /app

CMD ["uvicorn", "main:app", "--port", "8000", "--host", "127.0.0.1"]
