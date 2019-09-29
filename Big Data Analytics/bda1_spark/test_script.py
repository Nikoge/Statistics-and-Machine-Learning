# import pyspark
from pyspark import SparkContext

# create the spark application
sc = SparkContext(appName = "Exercise App")

# import the data
# temperature_file = sc.textFile("./temperature-readings.csv")
temperature_file = sc.textFile("../station_data/short_temperature_reads.csv")


# transform the data by splitting each line
lines = temperature_file. \
    map(lambda line: line.split(";"))


############
#####   1
############
# transform the data by extracting year and temperature as tuple
year_temperature = lines. \
    map(lambda x: (x[1][0:4], float(x[3])))

# filter data by year
year_temperature = year_temperature. \
    filter(lambda x: int(x[0])>=1950 and int(x[0])<=2014)

# reducer, to get the max temperature by KEY (year)
max_temperatures = year_temperature. \
    reduceByKey(max). \
    sortByKey(ascending=False)
# reducer, to get the min temperature by KEY (year)
min_temperatures = year_temperature. \
    reduceByKey(min). \
    sortByKey(ascending=False)

max_temperatures.saveAsTextFile("./res/max")
min_temperatures.saveAsTextFile("./res/min")

############
#####   1a
############

year_station_temp = lines. \
    map(lambda x: (x[1][0:4], (x[0], float(x[3]))))

year_temperature = year_station_temp. \
    filter(lambda x: int(x[0])>=1950 and int(x[0])<=2014)

max_temperatures = year_temperature. \
    reduceByKey(lambda a,b: a if a>b else b). \
    sortByKey(False)

min_temperatures = year_temperature. \
    reduceByKey(lambda a,b: b if a>b else a). \
    sortByKey(False)



max_temperatures.saveAsTextFile("./res/max_stations")
min_temperatures.saveAsTextFile("./res/min_stations")



############
#####   2.i
############

# map as ((year, month), (station_no, temp, 1))
year_month = lines. \
    map(lambda x: ((x[1][0:4],x[1][5:7]), (x[0], float(x[3]))))

# filter by constraints and put 1 as value
year_month = year_month. \
    filter(lambda x: int(x[0][0])>=1950 and int(x[0][0])<=2014 and x[1][1]>10)

# map as pair rdd (key,1) and count them, sort them
count_reads = year_month. \
    map(lambda x: (x[0], 1)). \
    reduceByKey(lambda x,y: x+y). \
    sortByKey(ascending=False)

count_reads.saveAsTextFile("./res/count_reads_month")


############
#####   2.ii
############
# get only one tuple for a station in one month.
# Remove duplicated reads in one month
year_month_unique = year_month. \
    map(lambda x: (x[0], (x[1][0], 1))). \
    distinct()

# map as pair rdd (key,1) and count them, sort them
station_month_counts = year_month_unique. \
    map(lambda x: (x[0], 1)). \
    reduceByKey(lambda x,y: x+y). \
    sortByKey(ascending=False)

count_reads.saveAsTextFile("./res/count_reads_month_distinct")


############
#####   3
############
# functions like reduceByKey which do smt with Value tuple use functions which
# gets arguments 2 elements (which represent tuple).
# in this example the line of monthly_avg we have a value tuple as (temp, 1)
# and the func that is used by reduceByKey takes x,y values.
# we want to sum all value pairs like (x_temp + y_temp, x_1+y_1) and store it
# as a value tuple again.
# YOU CANNOT DROP FIELDS! for example if you have 2 values in the values tuple
# you have to write a valur for each field you have otherwise you have to map again!

# map as (date, station_no), (temperature)
# to calculate average temp of each day
yr_mn_st = lines. \
    map(lambda x: ((x[1], x[0]), (float(x[3]))))

# calculate avg temp for each day by using defined formula
# avg of min of day and max of day
# we grouped it by key in order to apply function to days for each station seperately
daily_avg = yr_mn_st.groupByKey().mapValues(lambda x: (max(x)+min(x))/2)

# calculate average of month for each station
# map as (year, month, station_no), (daily_avg, 1)
# 1 for counting element count while summing
# sum temperature and count how many elements we have
# map it again to find the average
monthly_avg = daily_avg. \
    map(lambda x: ((x[0][0][0:4], x[0][0][5:7], x[0][1]), (x[1],1))). \
    reduceByKey(lambda x,y: (x[0] + y[0], x[1] + y[1])). \
    map(lambda x: (x[0], x[1][0]/x[1][1])). \
    sortByKey(False)

monthly_avg.filter(lambda x: int(x[0][0])>1960 and int(x[0][0])<2014). \
    saveAsTextFile("./res/avg_month")



############
#####   4
############

precipitation_file = sc.textFile("../station_data/short_precipitation-readings.csv")

# transform the data by splitting each line
lines_precipitation = precipitation_file. \
    map(lambda line: line.split(";"))


# map as (station_no, temp)
# find maximum read of station
station_temp = lines. \
    map(lambda x: (x[0], float(x[3]))). \
    reduceByKey(max)


# map as (station, precipitation)
# find max precipitation of station
station_precipitation = lines_precipitation. \
    map(lambda x: (x[0], float(x[3]))). \
    reduceByKey(max)


# join them
station_temp_prec = station_temp.join(station_precipitation)

# filter the last data for constraints
station_temp_prec.filter(lambda x: x[1][0]>25 and x[1][0]<30 \
    and x[1][1]>100 and x[1][1]<200)


############
#####   5
############

# import stations in Ostergotland
ost_station_file = sc.textFile("../station_data/stations-Ostergotland.csv")

# transform the data by splitting each line
lines_ost = ost_station_file. \
    map(lambda line: line.split(";"))

# get station_ids in Ostergotland as an Array
ost_station_ids = lines_ost. \
    map(lambda x: x[0]).collect()

# map as ((station_no, yyyy-mm), (precipitation, 1))
# filter only ostergotland stations and date constraint
# sum all values by reduceByKey
# map it again to find avg of month
ost_station_prec = lines_precipitation. \
    map(lambda x: ((x[0], x[1][0:4], x[1][5:7]), (float(x[3]), 1))). \
    filter(lambda x: x[0][0] in ost_station_ids and \
        int(x[0][1])>1993 and int(x[0][1])<2016). \
    reduceByKey(lambda x,y: (x[0]+y[0], x[1]+y[1])). \
    map(lambda x: (x[0], x[1][0]/x[1][1]))

ost_station_prec.saveAsTextFile("./res/avg_ost_station")


############
#####   6
############

# we use the avg temperature monthly that we found before in taks 3
# map as ((yyyy, mm),(avg_temp, 1))
# reduceByKey and found sum of values by keys
# map it again as ((yyyy, mm), avg) where avg is value[0]/value[1]
# sort them
monthly_avg50_14 = monthly_avg. \
    filter(lambda x: lambda x: x[0][2] in ost_station_ids and\
        int(x[0][0])>1950 and int(x[0][0])<2014).\
    map(lambda x: ((x[0][0], x[0][1]),(x[1], 1))). \
    reduceByKey(lambda x,y: (x[0]+y[0], x[1]+y[1])). \
    map(lambda x: (x[0], x[1][0]/x[1][1])). \
    sortByKey(ascending=False)

# filter again to get only before 1980
# map it as (mm, (avg_temp, 1))
# reduceByKey and found sum of values by keys
# map it again as (mm, avg)
# sort them
long_term_avg = monthly_avg50_14. \
    filter(lambda x: int(x[0][0])<1980). \
    map(lambda x: (x[0][1], (x[1], 1))). \
    reduceByKey(lambda x,y: (x[0]+y[0], x[1]+y[1])). \
    map(lambda x: (x[0], x[1][0]/x[1][1])). \
    sortByKey(ascending=False)
