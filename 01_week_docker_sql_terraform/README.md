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
  - Therefore, we will create a local conda environment, install our packages, and then export it to a yml file using the following command:
  - `conda env export --no-builds --from-history > environment.yml`
  - Then we will copy over the `environment.yml` to our container's filesystem using the following command:
  - `COPY environment.yml /app/`
  - Then we will recreate the environment inside our Docker container. To do so, we will add the following code to our Dockerfile to create a custom layer on top of the base `miniconda` image.
  - `RUN conda env update --name base --file /app/environment.yml && conda clean --all -y`
  - `RUN conda init bash`
- Write a Python script that will:
  - Download the datasets from the source URLs
  - Load the datasets into a usable format (ie. Pandas Dataframe)
  - Clean up and transform the data to be ready for export into the database
  - Set up a connection with the database
  - Generate the appropriate schema, if required, for the new tables
  - Iteratively chunk and load the transformed data into the database
  - Close the database connection and perform clean up.
- Setup a command to run the script when the container is instantiated. We will add the following command to our `docker-compose.yaml` file:
- `command:["python","script.py","--user","postgres", "--password","postgres","--host","db","--port","5432","--db","ny_taxi"]`

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

### Question 4: Longest trip each day

Which was the pick up day with the longest trip distance?

```
SELECT
	lpep_pickup_datetime
FROM
	green_taxi_trips AS trips
JOIN
	(SELECT
		MAX(trip_distance) AS dist
	FROM
		green_taxi_trips
	) AS max_dist
ON
	trips.trip_distance = max_dist.dist
```

**Answer**: 2019-10-31

### Question 5: Three biggest pickup zones

Which were the top pickup locations with over `13,000` in `total_amount` (across all trips) for 2019-10-18?

According to the question, we should only use `lpep_pickup_datetime` when filtering by date. Therefore, our SQL query will be:

```
SELECT
	"Zone"
FROM
	(SELECT
		"PULocationID",
		ROUND(SUM(total_amount)) AS total_amount
	FROM
		green_taxi_trips
	WHERE
		DATE_TRUNC('DAY', lpep_pickup_datetime) = DATE '2019-10-18'
	GROUP BY
		"PULocationID"
	ORDER BY
		total_amount DESC
	LIMIT 3) AS top_3

JOIN
	zones
ON
	"PULocationID" = "LocationID"
```

**Answer**: East Harlem North, East Harlem South, Morningside Heights

### Question 6: Largest tip

```
SELECT
	"DOLocationID",
	total_tip,
	"LocationID",
	"Zone"
FROM
	(SELECT
		"DOLocationID",
		MAX(tip_amount) AS total_tip
	FROM
		green_taxi_trips
	JOIN
		zones
	ON
		"PULocationID" = "LocationID"
	WHERE
		DATE_TRUNC('MONTH', lpep_pickup_datetime) = DATE_TRUNC('MONTH', DATE '2019-10-01')
		AND "Zone" = 'East Harlem North'
	GROUP BY
		"DOLocationID"
	ORDER BY
		total_tip DESC
	LIMIT
		1
	) AS max_tip
JOIN
	zones
ON
	"DOLocationID" = "LocationID"
```

**Answer**: JFK Airport

---

## Prepare Terraform

- Create a folder for terraform.
- Create a variables.tf to manage all config in one place.
- Download the GCP credentials and store it as a `cred_key.json` file in the terraform folder.
- In the project `.gitignore` file, ensure tha the key is not tracked.
- Save the path to the key as a variable in the variables.tf file.
- Add the provider plugin and write the resource requests in the main.tf file.
- From the terminal, go to the terraform folder.
- Run `terraform init` to setup terraform
- Run `terraform plan` to preview the changes in GCP
- Run `terraform apply` to deploy the changes and spin up resources
- Run `terraform destroy` to wind down resources and remove them from GCP.

---

### Question 7: Terraform Workflow

1. Downloading the provider plugins and setting up backend

- `terraform init`

2. Generating proposed changes and auto-executing the plan

- `terraform apply -auto-approve`

3. Remove all resources managed by terraform

- `terraform destroy`
