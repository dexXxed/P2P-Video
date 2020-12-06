FROM python:3.7-slim

WORKDIR /home

COPY templates ./templates
COPY services ./services
COPY * ./
RUN apt-get update
RUN pip install -r requirements.txt

ENTRYPOINT ["python", "app.py"]
