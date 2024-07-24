FROM python:3.11 AS builder

RUN curl -fsSL https://deb.nodesource.com/setup_16.x | bash -
RUN apt-get install -y nodejs

RUN pip install poetry
ENV POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=1 \
    POETRY_VIRTUALENVS_CREATE=1 \
    POETRY_CACHE_DIR=/tmp/poetry_cache
WORKDIR /app
COPY pyproject.toml poetry.lock ./
RUN poetry install --no-root && rm -rf $POETRY_CACHE_DIR

COPY ui/package.json ui/package-lock.json ./
RUN npm install

FROM python:3.11 AS runtime

RUN curl -fsSL https://deb.nodesource.com/setup_16.x | bash -
RUN apt-get install -y nodejs

ENV PATH="/app/.venv/bin:$PATH"
ENV PORT="8080"
COPY --from=builder /app/.venv /app/.venv
COPY --from=builder /app/node_modules /app/node_modules
COPY . ./
RUN prisma generate


# Bind the port and refer to the app.py app
# CMD exec gunicorn --bind :$PORT --workers 1 --worker-class uvicorn.workers.UvicornWorker  --threads 8 app.main:app
CMD exec gunicorn --bind :$PORT --workers 2 --timeout 0 --worker-class uvicorn.workers.UvicornWorker  --threads 8 app.main:app