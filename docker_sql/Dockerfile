#Base Image
FROM python:3.9.1
RUN apt-get update && apt-get install -y wget
RUN pip install pandas sqlalchemy psycopg requests


WORKDIR /app
COPY data_ingestion.py ingest_data.py 

ENTRYPOINT [ "python", "data_ingestion.py" ]