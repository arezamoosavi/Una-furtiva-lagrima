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


def create_initial_load(**kwargs):
    
    # scraper = CmcScraper("BTC", start_date="01-10-2021", end_date="3-10-2021")
    scraper = CmcScraper("BTC")
    headers, data = scraper.get_data()
    df = scraper.get_dataframe()
    
    sdf = spark.createDataFrame(df)

    sdf = raw_data_transforms(sdf)
    # sdf.printSchema()
    # sdf.show()
    write_postgres(sdf, "postgres", "admin", "admin", "bitcoin", "main_data", 6, "append")

    spark.stop()

    return "Done"


if __name__ == "__main__":

    create_initial_load()
