FROM python:3.9

WORKDIR /app

COPY pyproject.toml poetry.lock README.md /app/
COPY api /app/api

RUN pip install --no-cache-dir poetry

RUN poetry install --no-dev

EXPOSE 5000

CMD ["poetry", "run", "gunicorn", "api.app:create_app()", "-b", "0.0.0.0:5000"]
