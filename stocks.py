import pandas as pd
from datetime import datetime, timedelta

ticker = "nvda.us"                     #  U.S. stocks
end   = datetime.today()
start = end - timedelta(days=5*365)

url = f"https://stooq.com/q/d/l/?s={ticker}&d1={start:%Y%m%d}&d2={end:%Y%m%d}&i=d"
nvda = (pd.read_csv(url, parse_dates=["Date"])
           .set_index("Date")
           .sort_index())               # chronological order
print(nvda)


#pip install pandas
