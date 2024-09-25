# IMDb API with Flask and PySpark

This repository contains a Flask-based API that provides information about the top actors and the top 5 movies based on IMDb data processed using PySpark.

## Overview

The API interacts with processed IMDb data, including details about movies, actors, and calculated statistics. It exposes two endpoints:

1. **Top Actors Endpoint:** `/top_actors`
   - Provides information about the top actors based on the number of films they have participated in.

2. **Top Movies by Genre Endpoint:** `/top_movies_by_genre`
   - Offers information about the top 5 movies in each genre based on average ratings.

## Components

1. **PySpark Data Processing:**
   - Processes IMDb data to create a dataset of movies, actors, and associated information.
   - Calculates statistics, including the number of films per actor and average ratings per genre.

2. **Flask API:**
   - Provides two endpoints to fetch top actors and top movies by genre.
   - Returns data in JSON format for easy integration.

3. **Dockerized Deployment:**
   - Dockerfile and Makefile included for containerized deployment.

## Usage

### Prerequisites

- Docker installed on your machine.

### Running with Docker

1. Open a terminal and navigate to the root of your project.

2. Run the following command to build and start the services:

   ```bash
   make run

3. Access the API: Visit http://localhost:5000/top_actors and http://localhost:5000/top_movies_by_genre to interact with the API.


## Improved Architecture



### Event-Driven Architecture

We can explore an event-driven architecture using technologies like Apache Kafka or RabbitMQ. This pattern allows for asynchronous communication between services, decoupling Flask and Spark processes. It improves fault tolerance and supports real-time processing.

## Alternative Technologies

### Apache Flink

We can explore Apache Flink as an alternative to Apache Spark for stream processing. 

We can consider Dask, a parallel computing library, as an alternative to PySpark. Dask integrates seamlessly with Jupyter notebooks and provides a flexible parallel computing framework for data analysis.



