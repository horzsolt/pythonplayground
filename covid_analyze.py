import pandas as pd
import requests
import os

CSV_FILE = "owid-covid-data.csv"

if os.path.exists(CSV_FILE):
    os.remove(CSV_FILE)

response = requests.get("https://github.com/owid/covid-19-data/blob/master/public/data/owid-covid-data.csv?raw=true")
open(CSV_FILE, "wb").write(response.content)

try:
    df = pd.read_csv("owid-covid-data.csv", parse_dates=["date"])
    europe_df = df.query('continent == "Europe"')
    grouped_df = europe_df.groupby(df["location"])[["new_cases", "new_deaths", "new_deaths_per_million"]].sum()

    print(f"\nDeaths per million between {df['date'].min().strftime('%Y-%m-%d')} and {df['date'].max().strftime('%Y-%m-%d')}:\n")
    print(grouped_df.sort_values('new_deaths_per_million', ascending=False).nlargest(20, 'new_deaths_per_million').reset_index(drop=False))
finally:
    os.remove(CSV_FILE)
