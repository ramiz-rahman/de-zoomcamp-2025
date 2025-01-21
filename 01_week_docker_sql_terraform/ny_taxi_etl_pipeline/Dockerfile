FROM continuumio/miniconda3

WORKDIR /app

COPY pipeline.py pipeline.py

RUN conda install pandas sqlalchemy psycopg2 jupyter


# CMD ["python", "pipeline.py"]
