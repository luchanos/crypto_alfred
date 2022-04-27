FROM python:3.9.12-slim-buster
WORKDIR /
COPY . .
RUN pip install -r requirements.txt
CMD ["python", "main.py"]