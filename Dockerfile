FROM 3.9.12-slim-buster
WORKDIR /
COPY . .
CMD ["python", "main.py"]