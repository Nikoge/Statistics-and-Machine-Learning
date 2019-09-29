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

#task 2.1
#we create the sqp query grouping by year and month
#we use the function count in  the grouping tables
#finally we choose only the specific values and df_year_station
q1 = "SELECT year, month , count(value)\
FROM tempreadingstable \
WHERE value >10 and year BETWEEN 1950 AND 2014 \
group by year, month"

#we now want all the individual counts
q2 = "SELECT year, month, count(value) \
FROM (SELECT  distinct year, month,station, value \
FROM tempreadingstable \
WHERE value >=10 and year BETWEEN 1950 AND 2014) \
group by year, month \
order by (year, month) desc"

all_stations_count_monthly = sqlContext.sql(q1)
distinct_stations_count_monthly = sqlContext.sql(q2)



all_stations_count_monthly.rdd.saveAsTextFile("./bda2_res/all_stations_count_monthly")
distinct_stations_count_monthly.rdd.saveAsTextFile("./bda2_res/distinct_stations_count_monthly")
