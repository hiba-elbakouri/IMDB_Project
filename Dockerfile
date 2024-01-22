FROM jupyter/pyspark-notebook:latest

WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir -r requirements.txt

ENV SPARK_HOME=/usr/local/spark



USER root

RUN mkdir -p ./output

RUN chmod 700 ./output

VOLUME ./output ./output


RUN ["chmod", "+x", "./entrypoint.sh"]

ENTRYPOINT ["./entrypoint.sh"]

