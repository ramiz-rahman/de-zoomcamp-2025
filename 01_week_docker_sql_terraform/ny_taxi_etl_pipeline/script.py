import argparse

from ny_taxi_etl_pipeline.logging_config import setup_logging
from ny_taxi_etl_pipeline.utils import get_db_engine, download_csv
from ny_taxi_etl_pipeline.transformers import transform_pickup_dropoff_datetime
from ny_taxi_etl_pipeline.pipeline import etl_pipeline


def main(params):

    ### Setup Database Connection
    engine = get_db_engine(
        user=params.user,
        password=params.password,
        host=params.host,
        port=params.port,
        db=params.db,
    )

    #### ETL on Green Taxis
    taxis = {
        "url": "https://github.com/DataTalksClub/nyc-tlc-data/releases/download/green/green_tripdata_2019-10.csv.gz",
        "filename": "green-taxi-tripdata.csv.gz",
        "compression": "gzip",
    }
    taxi_filepath = download_csv(url=taxis["url"], filename=taxis["filename"])

    taxi_transformers = [transform_pickup_dropoff_datetime]

    if taxi_filepath:
        etl_pipeline(
            file_path=taxi_filepath,
            transformers=taxi_transformers,
            table_name="green_taxi_trips",
            con=engine,
        )

    #### ETL on Zones
    zones = {
        "url": "https://github.com/DataTalksClub/nyc-tlc-data/releases/download/misc/taxi_zone_lookup.csv",
        "filename": "taxi_zone_lookup.csv",
        "compression": None,
    }

    zones_filepath = download_csv(url=zones["url"], filename=zones["filename"])

    if taxi_filepath:
        etl_pipeline(
            file_path=zones_filepath,
            transformers=[],
            table_name="zones",
            con=engine,
        )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Download and ingest NY TAXI data to Postgres"
    )

    parser.add_argument("--user", help="User name for postgres")
    parser.add_argument("--password", help="Password for postgres")
    parser.add_argument("--host", help="Hostname for postgres")
    parser.add_argument("--port", help="Hostname for postgres")
    parser.add_argument("--db", help="Database name for postgres")

    args = parser.parse_args()

    setup_logging()

    main(args)


### Execution


#

# df_iter = pd.read_csv(
#     taxis["filename"], compression=taxis["compression"], chunksize=50000, iterator=True
# )
