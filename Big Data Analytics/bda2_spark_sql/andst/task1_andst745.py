
#import packages

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
schemaTempReadings.registerTempTable("tempReadingsTable")

df_year_station = schemaTempReadings.\
    where("year > 1950 and year < 2014").\
    groupBy('year',"station")

df_year_station_max = df_year_station.\
    agg(F.max('value').alias('max temperature')).\
    orderBy("max temperature", ascending= False)

df_year_station_min = df_year_station.\
    agg(F.min('value').alias('min temperature')).\
    orderBy("min temperature",ascending=False)


df_year_station_max.rdd.saveAsTextFile("./bda2_res/t1_max_stations")
df_year_station_min.rdd.saveAsTextFile("./bda2_res/t1_min_stations")
