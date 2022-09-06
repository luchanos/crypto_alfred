FROM python:3.9-slim-buster
COPY . .
WORKDIR .
RUN python3 -m pip install poetry
RUN poetry config virtualenvs.create false && poetry install
RUN python3 -m pip install connectors-0.1.0.tar.gz
RUN pybabel compile -d locales -D crypto_alfred
EXPOSE 10000
CMD ["python3", "telegram_bot.py"]
