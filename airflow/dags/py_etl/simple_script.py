
from cryptocmd import CmcScraper

# initialise scraper with time interval
# scraper = CmcScraper("XRP", "15-10-2017", "25-10-2017")

# initialise scraper without time interval
scraper = CmcScraper("BTC", start_date="01-10-2021", end_date="3-10-2021")

# get raw data as list of list
headers, data = scraper.get_data()
# print(headers)
# print(data)

# get data in a json format
json_data = scraper.get_data("json")

# export the data to csv
scraper.export("csv")

# get dataframe for the data
df = scraper.get_dataframe()
print(df.head())
print(df.tail())
print(df.shape)