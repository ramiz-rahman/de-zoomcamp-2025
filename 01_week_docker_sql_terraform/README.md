# HOMEWORK 1 Answers & Explanations

### Q1. Understanding Docker first run

- Command used: `docker run -i --entrypoint /bin/bash python:3.12.8`
- Docker downloads the python:3.12.8 image from Docker Hub and runs the container on my local machine. The entrypoint is set to the default bash shell, so that I can find out the version of pip being used.
- Find the version of pip inside this image: `pip --version`
- For our case, the result is `pip 24.3.1`

### Q2. Understanding Docker networking and docker-compose

- Answer: `db:5432`
- Since the two containers are loaded from within the same Docker network, courtesy of `docker compose`, the non forwarded, local port (i.e. second one in the `"-port:port"` ) should be used.
- The service identifier (`db`) should be used.

---

## Preparing Postgres with NY Taxi Data

We need to download the taxi data from some url and then set up a Python program (either a _Jupyter notebook_ or a _script_) to parse the data and load it into our Postgres database.

We can of course manually perform these steps one at a time and run everything on our host OS, but the goal is create automated data pipelines that can run on the cloud.

Thus, we are going to take the following approach:

- Create a custom container that will hold our data pipeline program
  - A container is a runnable instance of an image.
  - An image is defined by a Dockerfile.
  - To create the image, we create our `Dockerfile`
- Setup the container with all necessary programs and packages to download, parse and write to our database
  - Some packages, such as `psycopg2` cause problems when installed with `pip`. In order to avoid these complications, and make our lives simpler, we will be using `miniconda` as our base image.
  - `FROM continuumio/miniconda3`
  - Since we will be manipulating CSV data and connecting to a Postgres database, we will need the `pandas`, `sqlalchemy`, and `psycopg2` packages.
  - Therefore, we add the following line to our Dockerfile to create a custom layer on top of the base `miniconda` image.
  - `RUN conda install pandas sqlalchemy psycopg2`
- Write a Python script that will:
  - Download the datasets from the source URLs
  - Load the datasets into a usable format (ie. Pandas Dataframe)
  - Clean up and transform the data to be ready for export into the database
  - Set up a connection with the database
  - Generate the appropriate schema, if required, for the new tables
  - Iteratively chunk and load the transformed data into the database
  - Close the database connection and perform clean up.
- Setup a command to run the script when the container is instantiated

---

### Q3 Trip Segmentation Count

The number of trips that happened during the period of October 1st 2019 (inclusive) and November 1st 2019 (exclusive).

To get all the trips, we can run the following query.

```
SELECT
	*
FROM
	green_taxi_trips
WHERE
	lpep_pickup_datetime >= DATE '2019-10-01'
	AND lpep_dropoff_datetime < DATE '2019-11-01'
ORDER BY
	lpep_pickup_datetime, lpep_dropoff_datetime
```

If we just want the number, we can use the `COUNT` aggregate function and remove the `ORDER BY` clause.

```
SELECT
	COUNT(*)
FROM
	green_taxi_trips
WHERE
	lpep_pickup_datetime >= DATE '2019-10-01'
	AND lpep_dropoff_datetime < DATE '2019-11-01'
```

**Answer**: 476,196

#### Trips up To 1 Mile

Based on the [data dictionary](https://www.nyc.gov/assets/tlc/downloads/pdf/data_dictionary_trip_records_green.pdf), the `trip_distance` column gives us the trip distance in miles.

Thus our query will be:

```
SELECT
	COUNT(*)
FROM
	green_taxi_trips
WHERE
	lpep_pickup_datetime >= DATE '2019-10-01'
	AND lpep_dropoff_datetime < DATE '2019-11-01'
	AND trip_distance <= 1.00
```

**Answer**: 104,802

#### Trips in between 1 (exclusive) and 3 miles (inclusive)

```
SELECT
	COUNT(*)
FROM
	green_taxi_trips
WHERE
	lpep_pickup_datetime >= DATE '2019-10-01'
	AND lpep_dropoff_datetime < DATE '2019-11-01'
	AND (trip_distance > 1.00 AND trip_distance <= 3.00)
```

**Answer**: 198,924

#### Trips in between 3 (exclusive) and 7 miles (inclusive)

```
SELECT
	COUNT(*)
FROM
	green_taxi_trips
WHERE
	lpep_pickup_datetime >= DATE '2019-10-01'
	AND lpep_dropoff_datetime < DATE '2019-11-01'
	AND (trip_distance > 3.00 AND trip_distance <= 7.00)
```

**Answer**: 109,603

#### Trips in between 7 (exclusive) and 10 miles (inclusive)

```
SELECT
	COUNT(*)
FROM
	green_taxi_trips
WHERE
	lpep_pickup_datetime >= DATE '2019-10-01'
	AND lpep_dropoff_datetime < DATE '2019-11-01'
	AND (trip_distance > 7.00 AND trip_distance <= 10.00)
```

**Answer**: 27,678

#### Trips over 10 miles

```
SELECT
	COUNT(*)
FROM
	green_taxi_trips
WHERE
	lpep_pickup_datetime >= DATE '2019-10-01'
	AND lpep_dropoff_datetime < DATE '2019-11-01'
	AND trip_distance > 10.00
```

**Answer**: 35,189

So our final answer will be: `104,802; 198,924; 109,603; 27,678; 35,189`
