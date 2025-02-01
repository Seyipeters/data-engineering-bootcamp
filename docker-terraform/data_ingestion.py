#import the required libraries
import os
import pandas as pd
from sqlalchemy import create_engine
from time import time
import argparse
import requests

# Argument parser
parser = argparse.ArgumentParser(description='Ingest CSV data to Postgres')
parser.add_argument('--user', required=True, help='User name for Postgres')
parser.add_argument('--password', required=True, help='Password for Postgres')
parser.add_argument('--host', required=True, help='Host for Postgres')
parser.add_argument('--port', required=True, help='Port for Postgres')
parser.add_argument('--db', required=True, help='Database name for Postgres')
parser.add_argument('--table_name', required=True, help='Name of the table to write results to')
parser.add_argument('--url', required=True, help='URL of the CSV file')

args = parser.parse_args()


def main(params):
    user = params.user
    password = params.password
    host = params.host
    port = params.port
    db = params.db
    table_name = params.table_name
    url = params.url
    
    #Extract the file name from the URL
    csv_name = url.split('/')[-1]

    # Download the CSV file
    print(f"Downloading {csv_name} from {url}... ")
    response = requests.get(url)
    with open(csv_name, 'wb') as f:
        f.write(response.content)
    print("Download complete: {csv_name}")
    

    # Create a connection to the PostgreSQL database
    engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{db}')

    # Read the CSV in chunks
    df_iter = pd.read_csv(csv_name, iterator=True, chunksize=100000)

    # Extract the first chunk
    df = next(df_iter)

    # Convert date columns to datetime format (if applicable)
    if 'tpep_pickup_datetime' in df.columns:
        df.tpep_pickup_datetime = pd.to_datetime(df.tpep_pickup_datetime)
    if 'tpep_dropoff_datetime' in df.columns:
        df.tpep_dropoff_datetime = pd.to_datetime(df.tpep_dropoff_datetime)

    # Create the table schema in the database (if not exists)
    df.head(0).to_sql(name=table_name, con=engine, if_exists='replace')
    df.to_sql(name=table_name, con=engine, if_exists='append')

    # Load data in chunks
    while True:
        try:
            t_start = time()  # Record the start time
            df = next(df_iter)

            # Convert date columns to datetime format
            df.tpep_pickup_datetime = pd.to_datetime(df.tpep_pickup_datetime)
            df.tpep_dropoff_datetime = pd.to_datetime(df.tpep_dropoff_datetime)

            # Append the chunk to the database
            df.to_sql(name=table_name, con=engine, if_exists='append')

            t_end = time()  # Record the end time
            print(f'Inserted another chunk, took {t_end - t_start:.3f} seconds')

        except StopIteration:
            print("All data has been imported successfully")
            break
        except Exception as e:
            print(f"An error occurred: {e}")
            break


if __name__ == '__main__':
    main(args)
