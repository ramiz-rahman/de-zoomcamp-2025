from ny_taxi_etl_pipeline.logging_config import setup_logging
from ny_taxi_etl_pipeline.utils import get_db_engine, download_csv
from ny_taxi_etl_pipeline.transformers import transform_pickup_dropoff_datetime
from ny_taxi_etl_pipeline.pipeline import etl_pipeline


def main():

    ### Setup Database Connection
    engine = get_db_engine(
        user="postgres",
        password="postgres",
        host="localhost",
        port="5433",
        db="ny_taxi",
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
    setup_logging()
    main()
    # taxis = {
    #     "url": "https://github.com/DataTalksClub/nyc-tlc-data/releases/download/green/green_tripdata_2019-10.csv.gz",
    #     "filename": "green-taxi-tripdata.csv.gz",
    #     "compression": "gzip",
    # }
    # taxi_filepath = download_csv(url=taxis["url"], filename=taxis["filename"])
    # if taxi_filepath:
    #     df_iter = extract(taxi_filepath)
    #     for df in df_iter:
    #         print(len(df))


### Execution


#

# df_iter = pd.read_csv(
#     taxis["filename"], compression=taxis["compression"], chunksize=50000, iterator=True
# )
