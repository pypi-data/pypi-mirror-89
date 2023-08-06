from pyspark.sql import SparkSession
from pyspark.sql.functions import col
from udrparser.parsewebpagedoc import udrparser
import warnings

warnings.simplefilter(action="ignore", category=Warning)


class performnslookup:
    def dowork():
        spark = SparkSession.builder.getOrCreate()
        outputdf = udrparser.getdoctables()
        outputdf["IPAddress"] = outputdf["Azure Databricks Workspace Region"].map(
            lambda host: udrparser.tryconvert(host) if host is not None else host
        )
        sdf = spark.createDataFrame(outputdf)
        sdf.createOrReplaceTempView("UDR")
        outdf = spark.sql("SELECT * FROM UDR").filter(
            col("Azure Databricks Workspace Region") != ""
        )
        outdf.createOrReplaceTempView("UDR")
        return outdf
