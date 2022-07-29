FROM python:3.9.12-slim-buster
WORKDIR /
COPY pyproject.toml poetry.lock
RUN poetry config virtualenvs.create false && poetry install --no-root
CMD ["python", "main.py"]