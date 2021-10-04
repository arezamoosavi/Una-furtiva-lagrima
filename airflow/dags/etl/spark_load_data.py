import os
import sys
import logging

from common import get_spark_session, write_postgres, raw_data_transforms

from cryptocmd import CmcScraper


# spark session
spark = get_spark_session("Raw Data")
# Set log4j
spark.sparkContext.setLogLevel("ERROR")
log4jLogger = spark._jvm.org.apache.log4j
logger = log4jLogger.LogManager.getLogger("LOGGER")
logger.setLevel(log4jLogger.Level.INFO)


def create_initial_load(start_date=None, end_date=None,**kwargs):
    
    scraper = CmcScraper("BTC", start_date=start_date, end_date=end_date)
    headers, data = scraper.get_data()
    df = scraper.get_dataframe()
    
    sdf = spark.createDataFrame(df)

    sdf = raw_data_transforms(sdf)
    sdf.printSchema()
    sdf.orderBy("ref_date", ascending=True).show(3)
    
    write_postgres(sdf, "postgres", "admin", "admin", "bitcoin", "main_data", 1, "append")

    spark.stop()

    return "Done"


if __name__ == "__main__":
    
    if len(sys.argv) == 1:
        start_date=None
        end_date=None
    else:
        start_date = "-".join(str(sys.argv[1]).split("-")[::-1])
        end_date = "-".join(str(sys.argv[2]).split("-")[::-1])
    
    create_initial_load(start_date, end_date)
