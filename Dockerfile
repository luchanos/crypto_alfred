FROM python:3.9-slim-buster
COPY . .
WORKDIR .
RUN python3 -m pip install poetry
RUN python3 -m pip install connectors-0.1.0.tar.gz
RUN poetry config virtualenvs.create false && poetry install
RUN pybabel extract . -o locales/crypto_alfred.pot
RUN pybabel update -d locales -D crypto_alfred -i locales/crypto_alfred.pot
RUN pybabel compile -d locales -D crypto_alfred
EXPOSE 10000
CMD ["python3", "telegram_bot.py"]
