FROM python:3.9-slim-buster
COPY . .
WORKDIR .
RUN python3 -m pip install -r requirements.txt
RUN python3 -m pip install connectors-0.1.0.tar.gz
EXPOSE 5000
CMD ["python3", "main.py"]
