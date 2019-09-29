#introductory commands
from pyspark import SparkContext
from pyspark.sql import SQLContext, Row
from pyspark.sql import functions as F

sc = SparkContext()
sqlContext = SQLContext(sc)

#import the data
temperature_file = sc.textFile("../station_data/short_temperature_reads.csv")
lines = temperature_file.map(lambda line: line.split(";"))

#names of the columns
tempReadingsString = ["station", "date", "year", "month", "time", "value",
"quality"]

tempReadingsRow = lines.map(lambda p: (p[0], p[1], int(p[1].split("-")[0]),
int(p[1].split("-")[1]), p[2], float(p[3]), p[4] ))


# Apply the schema to the RDD.
schemaTempReadings = sqlContext.createDataFrame(tempReadingsRow,
tempReadingsString)

# Register the DataFrame as a table.
schemaTempReadings.registerTempTable("tempreadingstable")

######## Task 3#######

df_min_max = schemaTempReadings.\
    where("year >=1960 and year<=2014").\
    groupBy("date","year","month","station").\
    agg(((F.max('value') + F.min("value"))/2).alias("avg daily")).\
    groupBy("year","month","station").\
    agg(F.avg("avg daily").alias("avg monthly"))

#another way using select function
#df_min_max.withColumn("average", (df_min_max.max_value + df_min_max.min_value)/2
#df_min_max.select("year","month","station",(df_min_max.max_value + df_min_max.min_value)/2).alias("avg monthly")




    withColumn("ave",$"max(value)"+$"min(value)").show()
