import os
import sys
import logging

from pyspark import StorageLevel
from pyspark.sql import SparkSession
from pyspark.sql import functions as F


def get_spark_session(appname):

    spark = (SparkSession.builder
             .appName(appname)
             .config("spark.network.timeout", "10000s")
             .getOrCreate())
    return spark

def raw_data_transforms(sdf):
    sdf = sdf.withColumn("ref_date", sdf["Date"].cast("date"))
    sdf = sdf.withColumnRenamed("Market Cap", "market_cap")
        
    sdf = sdf.select([F.col(x).alias(x.lower()) for x in sdf.columns])
    sdf = sdf.select(["ref_date", "open", "high", "low", "close", "volume", "market_cap"])
    
    return sdf

def write_postgres(sdf, host, user, password, database, table, partition=16, mode="append"):
    pg_properties = {
        "driver": "org.postgresql.Driver",
        "user": user,
        "password": password}
    pg_url = "jdbc:postgresql://{}:5432/{}".format(host, database)

    (sdf
    #  .orderBy(["ref_date"], ascending=[1])
     .repartition(partition).sortWithinPartitions("ref_date")
     .write.jdbc(url=pg_url, table=table, mode=mode, properties=pg_properties))

def read_postgres(spark, host, user, password, database, table):
    return (spark.read \
            .format("jdbc") \
            .option("url", "jdbc:postgresql://{0}/{1}?user={2}&password={3}".format(host, database, user, password)) \
            .option("driver", "org.postgresql.Driver") \
            .option("query", "SELECT * FROM {}".format(table)) \
            .load())