import os
import sys
import logging

from common import get_spark_session, write_postgres, read_postgres

# spark session
spark = get_spark_session("Raw Data")
# Set log4j
spark.sparkContext.setLogLevel("ERROR")
log4jLogger = spark._jvm.org.apache.log4j
logger = log4jLogger.LogManager.getLogger("LOGGER")
logger.setLevel(log4jLogger.Level.INFO)


def create_bitcoin_facts(**kwargs):
    
    sdf = read_postgres(spark, "postgres", "admin", "admin", "bitcoin", "main_data")
    sdf = raw_data_transforms(sdf)
    # sdf.printSchema()
    # sdf.show()
    write_postgres(sdf, "postgres", "admin", "admin", "bitcoin", "fact_data", 6, "append")

    spark.stop()

    return "Done"


if __name__ == "__main__":

    create_initial_load()
