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

### Separation of Concerns

We can onsider separating concerns by deploying Flask and Jupyter services as independent microservices. Use Docker Compose to manage containers for each service. This provides better scalability, maintainability, and allows for independent updates.

### Event-Driven Architecture

We can explore an event-driven architecture using technologies like Apache Kafka or RabbitMQ. This pattern allows for asynchronous communication between services, decoupling Flask and Spark processes. It improves fault tolerance and supports real-time processing.

## Alternative Technologies

### Apache Flink

We can explore Apache Flink as an alternative to Apache Spark for stream processing. Flink offers low-latency and high-throughput stream processing capabilities. Evaluate its suitability for real-time analytics.

### Dask

We can consider Dask, a parallel computing library, as an alternative to PySpark. Dask integrates seamlessly with Jupyter notebooks and provides a flexible parallel computing framework for data analysis.

### Kubernetes

We can evaluate Kubernetes for container orchestration. Kubernetes simplifies deployment, scaling, and management of containerized applications. Consider using Kubernetes to manage Flask, Jupyter, and distributed data processing components.

## Deployment Patterns

### Serverless Architecture

We can consider a serverless architecture using AWS Lambda or Azure Functions for specific tasks. This approach can help with cost optimization, as resources are only provisioned when functions are executed.

### Data Lake Architecture

We can explore a data lake architecture for storing and processing large datasets. Utilize technologies like Apache Hudi or Apache Iceberg for managing incremental data updates efficiently.

## Advantages and Disadvantages of Using a Distributed Data Processing Framework



### Advantages

1. **Scalability:**
   - *Advantage:* Distributed frameworks can scale horizontally, efficiently handling large datasets by leveraging multiple nodes in a cluster.

2. **Performance:**
   - *Advantage:* Parallel processing and in-memory computation significantly improve performance, crucial for complex data analysis tasks.

3. **Fault Tolerance:**
   - *Advantage:* Distributed frameworks provide built-in fault tolerance mechanisms, ensuring reliability in the face of node failures.

4. **Ease of Use:**
   - *Advantage:* Higher-level APIs and abstractions, such as PySpark, simplify the development of complex data processing and analysis workflows.

5. **Versatility:**
   - *Advantage:* Distributed frameworks are versatile, capable of handling various data processing tasks, including ETL, machine learning, and graph processing.

### Disadvantages

1. **Complexity:**
   - *Disadvantage:* Working with distributed systems introduces additional complexity in terms of setup, configuration, and maintenance, requiring knowledge of distributed computing concepts.

2. **Resource Management:**
   - *Disadvantage:* Efficient resource management becomes crucial. Allocating and managing resources effectively can be challenging.

3. **Overhead:**
   - *Disadvantage:* Additional overhead is associated with distributed computing, such as communication between nodes and data shuffling, which can impact performance.

4. **Learning Curve:**
   - *Disadvantage:* Developers may face a learning curve when transitioning to distributed frameworks, understanding distributed concepts, optimizing performance, and troubleshooting issues.

5. **Cost:**
   - *Disadvantage:* Setting up and maintaining a distributed cluster infrastructure can be costly in terms of both hardware and operational expenses, which may not be justified for smaller-scale projects.
