#introductory commands
from pyspark import SparkContext
from pyspark.sql import SQLContext, Row
from pyspark.sql import functions as F

sc = SparkContext()
sqlContext = SQLContext(sc)

#import the data(temperature)
temperature_file = sc.textFile("../station_data/short_temperature_reads.csv")
lines = temperature_file.map(lambda line: line.split(";"))

#import the data(precipitation)
precipitation_file = sc.textFile("../station_data/short_precipitation-readings.csv")
lines_precipitation = precipitation_file.map(lambda line: line.split(";"))

#names of the columns
tempReadingsString = ["station", "date", "year", "month", "time", "value",
"quality"]

tempReadingsRow = lines.map(lambda p: (p[0], p[1], int(p[1].split("-")[0]),
int(p[1].split("-")[1]), p[2], float(p[3]), p[4] ))

#for precipitation
precReadingsRow = lines_precipitation.map(lambda p: (p[0], p[1], int(p[1].split("-")[0]),
int(p[1].split("-")[1]), p[2], float(p[3]), p[4] ))


# Apply the schema to the RDD.
schemaTempReadings = sqlContext.createDataFrame(tempReadingsRow,
tempReadingsString)

# Register the DataFrame as a table.
schemaTempReadings.registerTempTable("tempreadingstable")

# Apply the schema to the RDD for precipitatiion.
schemaPrecReadings = sqlContext.createDataFrame(precReadingsRow,
tempReadingsString)

# Register the DataFrame as a table.
schemaPrecReadings.registerTempTable("precreadingstable")

############## TASK 4 #######################################

#first we want the maximum temperature for each station
max_temp_station = schemaTempReadings.\
    groupBy("station").\
    agg(F.max('value').alias('max_temperature')).\
    where("max_temperature > 25 and max_temperature <30")

max_daily_prec = schemaPrecReadings.\
    groupBy("date","station").\
    agg(F.sum("value").alias("daily_prec")).\
    groupBy("station").\
    agg(F.max('daily_prec').alias('max_prec')).\
    where("max_prec > 100 and max_prec <200")

max_values = max_temp_station.\
    join(max_daily_prec,"station")
