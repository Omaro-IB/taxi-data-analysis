import pandas as pd
import glob
import pyarrow.parquet as pq
from tqdm import tqdm
import sys

def remove_wrong_years(df, year, verbose=True):
    invalid_years = []
    for index, row in tqdm(df.iterrows(), total=len(df)):
        if row['tpep_pickup_datetime'].year != year or row['tpep_dropoff_datetime'].year != year:
            invalid_years.append(index)

    if verbose and invalid_years:
        print(f"removed years {invalid_years}")
    df.drop(df.index[invalid_years], inplace=True)


for year in (2023, 2024):
    for month in range(1, 13):
        print(f"======= {year}-{month:02} =======")
        df = pd.read_parquet(f"data/{year}/yellow_tripdata_{year}-{month:02}.parquet")

        remove_wrong_years(df, 2023)
        df = df.drop_duplicates()
        df['yyyy-mm'] = f'{year}-{month:02}'

        df.to_parquet(f"data/{year}/yellow_tripdata_{year}-{month:02}-cleaned.parquet")

