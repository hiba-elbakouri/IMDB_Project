#!/bin/sh
wget -nc "https://datasets.imdbws.com/title.basics.tsv.gz" -P ./output/
wget -nc "https://datasets.imdbws.com/title.principals.tsv.gz" -P ./output/
wget -nc "https://datasets.imdbws.com/title.ratings.tsv.gz" -P ./output/
wget -nc "https://datasets.imdbws.com/name.basics.tsv.gz" -P ./output/
spark-submit --master local entrypoint.py
python app.py