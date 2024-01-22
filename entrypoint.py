if __name__ == '__main__':
    from pyspark.sql import SparkSession
    import pandas as pd

    from sqlalchemy import create_engine, Column, Integer, String

    from sqlalchemy.orm import declarative_base

    from pyspark.sql import SparkSession
    from pyspark.sql.functions import col
    from pyspark.sql.types import IntegerType
    from datetime import datetime

    from pyspark.sql import SparkSession
    from pyspark.sql.functions import col, avg, count
    from pyspark.sql.window import Window
    from pyspark.sql import functions as F

    from pyspark.errors.exceptions.captured import AnalysisException

    spark = SparkSession \
        .builder \
        .appName("IMDbAnalysis") \
        .getOrCreate()

    spark.sparkContext.setLogLevel("ERROR")

    ratings_df = spark.read.option("delimiter", "\t").csv("./output/title.ratings.tsv.gz", header=True,
                                                          inferSchema=True)
    principals_df = spark.read.option("delimiter", "\t").csv("./output/title.principals.tsv.gz", header=True,
                                                             inferSchema=True)
    basics_df = spark.read.option("delimiter", "\t").csv("./output/title.basics.tsv.gz", header=True, inferSchema=True)
    names_df = spark.read.option("delimiter", "\t").csv("./output/name.basics.tsv.gz", header=True, inferSchema=True)

    ratings_df = ratings_df.select("tconst", "averageRating", "numVotes")
    principals_df = principals_df.select("tconst", "nconst", "category", "job", "characters")
    basics_df = basics_df.select("tconst", "titleType", "primaryTitle", "originalTitle", "startYear", "runtimeMinutes",
                                 "genres")
    names_df = names_df.select("nconst", "primaryName", "birthYear", "deathYear", "primaryProfession", "knownForTitles")

    try:
        ratings_df.write.parquet("./output/title.ratings.parquet")
    except AnalysisException:
        pass

    try:
        principals_df.write.parquet("./output/title.principals.parquet")
    except AnalysisException:
        pass

    try:
        basics_df.write.parquet("./output/title.basics.parquet")
    except AnalysisException:
        pass

    try:
        names_df.write.parquet("./output/name.basics.parquet")
    except AnalysisException:
        pass

    Base = declarative_base()

    database_url = 'sqlite:///output/imdb_database.db'
    engine = create_engine(database_url, echo=True)


    class Movie(Base):
        __tablename__ = 'movie'
        tconst = Column(String, primary_key=True)
        titleType = Column(String)
        primaryTitle = Column(String)
        originalTitle = Column(String)
        startYear = Column(Integer)
        runtimeMinutes = Column(Integer)
        genres = Column(String)


    class Actor(Base):
        __tablename__ = 'top_actors'
        nconst = Column(String, primary_key=True)
        primaryName = Column(String)
        FilmCount = Column(Integer)


    class Movie(Base):
        __tablename__ = 'top_movies'
        genres = Column(String, primary_key=True)
        primaryTitle = Column(String)
        AverageRating = Column(Integer)
        MovieCount = Column(Integer)


    movies_df = pd.read_parquet("./output/title.basics.parquet")

    movies_df.to_sql('movies', con=engine, if_exists='replace', index=False)

    movies_df = pd.read_parquet("./output/title.basics.parquet")

    movies_df.to_sql('movies', con=engine, if_exists='replace', index=False)


    def parse_start_year(start_year):
        try:
            return datetime.strptime(str(start_year), '%Y').year
        except ValueError:
            return None



    title_basics_file = './output/title.basics.parquet'
    title_basics_df = spark.read.parquet(title_basics_file)

    title_principals_file = './output/title.principals.parquet'
    title_principals_df = spark.read.parquet(title_principals_file)

    name_basics_file = './output/name.basics.parquet'
    name_basics_df = spark.read.parquet(name_basics_file)

    merged_df = title_basics_df.join(title_principals_df, on='tconst')

    parse_start_year_udf = spark.udf.register("parse_start_year", parse_start_year, IntegerType())

    merged_df = (merged_df
                 .withColumn("start_year", parse_start_year_udf("startYear"))
                 .filter((col('titleType') == 'movie') &
                         (col('start_year').isNotNull()) & (col('start_year') >= 2010) &
                         (col('category') == 'actor')))

    merged_df = merged_df.join(name_basics_df, on='nconst')

    actor_film_counts = (merged_df
                         .groupBy('nconst', 'primaryName')
                         .agg({'tconst': 'count'})
                         .withColumnRenamed('count(tconst)', 'FilmCount'))

    sorted_actors = actor_film_counts.sort('FilmCount', ascending=False)

    top_actors = sorted_actors.limit(10)

    top_actors_pd = top_actors.toPandas()
    top_actors_pd.to_sql('top_actors', con=engine, if_exists='replace', index=False)


    title_basics_file = './output/title.basics.parquet'
    title_basics_df = spark.read.parquet(title_basics_file)

    title_ratings_file = './output/title.ratings.parquet'
    title_ratings_df = spark.read.parquet(title_ratings_file)

    merged_df = title_basics_df.join(title_ratings_df, on='tconst')

    parse_start_year_udf = F.udf(parse_start_year)

    filtered_df = (merged_df
                   .withColumn("start_year", parse_start_year_udf("startYear"))
                   .filter((col('titleType') == 'movie') & col('start_year').isNotNull() & (col('start_year') >= 2010)))

    genre_stats = (filtered_df
                   .groupBy('genres', 'primaryTitle')
                   .agg(avg('averageRating').alias('AverageRating'), count('tconst').alias('MovieCount')))

    window_spec = Window().partitionBy('genres').orderBy(col('AverageRating').desc())
    ranked_movies = genre_stats.withColumn('Rank', F.dense_rank().over(window_spec))

    top_movies_by_genre = ranked_movies.filter(col('Rank') <= 5).select('genres', 'primaryTitle', 'AverageRating',
                                                                        'MovieCount')

    top_movies_pd = top_movies_by_genre.toPandas()
    top_movies_pd.to_sql('top_movies', con=engine, if_exists='replace', index=False)