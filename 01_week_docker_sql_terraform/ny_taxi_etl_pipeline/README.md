### ELT Pipeline for NY Taxi Data

This package exist to seed our Postgres database with NY_TAXI data so that we can perform further analysis.

- Download the datasets from the source URLs
- Load the datasets into a usable format (ie. Pandas Dataframe)
- Clean up and transform the data to be ready for export into the database
- Set up a connection with the database
- Generate the appropriate schema, if required, for the new tables
- Iteratively chunk and load the transformed data into the database
- Close the database connection and perform clean up.
- Setup a command to run the script when the container is instantiated
