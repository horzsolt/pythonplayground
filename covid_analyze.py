import pandas as pd
import requests
import os
from datetime import datetime
import urllib

def analyze_covid_data():
    CSV_FILE = "owid-covid-data.csv"

    if os.path.exists(CSV_FILE):
        os.remove(CSV_FILE)

    urllib.request.urlretrieve("https://github.com/owid/covid-19-data/blob/master/public/data/owid-covid-data.csv?raw=true", CSV_FILE)

    try:
        df = pd.read_csv(CSV_FILE, parse_dates=["date"])
        europe_df = df.query('continent == "Europe"')
        grouped_df = europe_df.groupby(df["location"])[["new_cases", "new_deaths", "new_deaths_per_million"]].sum()

        print(f"\nDeaths per million between {df['date'].min().strftime('%Y-%m-%d')} and {df['date'].max().strftime('%Y-%m-%d')}:\n")
        print(grouped_df.sort_values('new_deaths_per_million', ascending=False).nlargest(20, 'new_deaths_per_million').reset_index(drop=False))
    finally:
        os.remove(CSV_FILE)

def analyze_stock_data(start_date, end_date):

    starttimestamp = str(round(datetime.timestamp(datetime.fromisoformat(start_date))))
    endtimestamp = str(round(datetime.timestamp(datetime.fromisoformat(end_date))))

    CSV_FILE = "stock.csv"

    if os.path.exists(CSV_FILE):
        os.remove(CSV_FILE)

    url= f"https://query1.finance.yahoo.com/v7/finance/download/CLDR?period1={starttimestamp}&period2={endtimestamp}&interval=1d&events=history&includeAdjustedClose=true"
    print(url)
    urllib.request.urlretrieve(url, CSV_FILE)

    try:
        pd.set_option('float_format', '{:,.2f}'.format)
        df = pd.read_csv(CSV_FILE, parse_dates=["Date"])

        print(df.Volume.describe())

    finally:
        os.remove(CSV_FILE)

analyze_covid_data()
print("==================================================================")
analyze_stock_data("2020-01-01", "2020-12-31")