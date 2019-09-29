#introductory commands
from pyspark import SparkContext
from pyspark.sql import SQLContext, Row
from pyspark.sql import functions as F

sc = SparkContext()
sqlContext = SQLContext(sc)

#First dataset for precipitation
#import the data(precipitation)
precipitation_file = sc.textFile("../station_data/short_precipitation-readings.csv")
lines_precipitation = precipitation_file.map(lambda line: line.split(";"))

#names of the columns
tempReadingsString = ["station", "date", "year", "month", "time", "value",
"quality"]

#for precipitation
precReadingsRow = lines_precipitation.map(lambda p: (p[0], p[1], int(p[1].split("-")[0]),
int(p[1].split("-")[1]), p[2], float(p[3]), p[4] ))

# Apply the schema to the RDD for precipitatiion.
schemaPrecReadings = sqlContext.createDataFrame(precReadingsRow,
tempReadingsString)

# Register the DataFrame as a table.
schemaPrecReadings.registerTempTable("precreadingstable")

#Second dataset for ostergotan
Ostergotland_file = sc.textFile("../station_data/stations-Ostergotland.csv")
lines_ostergotland = Ostergotland_file.map(lambda line: line.split(";"))


OsterReadingsString = ["station", "station_name"]

OsterReadingsRow = lines_ostergotland.map(lambda line: (line[0],line[1]))

# Apply the schema to the RDD for precipitatiion.
schemaOsteReadings = sqlContext.createDataFrame(OsterReadingsRow,
OsterReadingsString)

# Register the DataFrame as a table.
schemaOsteReadings.registerTempTable("Ostereadingstable")

############## TASK 5 #######################################

avg_monthly = schemaOsteReadings.\
    join(schemaTempReadings,"station").\
    where("year > 1993 and year < 2016").\
    groupBy("year","month").\
    agg(F.avg('value').alias('avg prec')).\
    orderBy("year","month", ascending = False)
