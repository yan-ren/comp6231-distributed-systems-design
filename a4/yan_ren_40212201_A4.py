import os
from itertools import permutations

from pyspark import RDD, SparkContext
from pyspark.sql import DataFrame, SparkSession
from pyspark.sql.functions import col


def restaurant_shift_coworkers(worker_shifts: RDD) -> RDD:
    """
    Takes an RDD that represents the contents of the worker_shifts.txt. Performs a series of MapReduce operations via
    PySpark to calculate the number of shifts worked together by each pair of co-workers. Returns the results as an RDD
    sorted by the number of shifts worked together THEN by the names of co-workers in a DESCENDING order.
    :param worker_shifts: RDD object of the contents of worker_shifts.txt.
    :return: RDD of pairs of co-workers and the number of shifts they worked together sorted in a DESCENDING order by
             the number of shifts then by the names of co-workers.
             Example output: [(('Shreya Chmela', 'Fabian Henderson'), 3),
                              (('Fabian Henderson', 'Shreya Chmela'), 3),
                              (('Shreya Chmela', 'Leila Jager'), 2),
                              (('Leila Jager', 'Shreya Chmela'), 2)]
    """
    def pair(x):
        item = x[1].split(',')
        res = []
        if len(item) == 1:
            return [((item[0], ), 1)]
        else:
            for i in item:
                for j in item:
                    if i != j:
                        res.append(((i, j), 1))

            return res


    worker_split = worker_shifts.map(lambda x: (x.split(",")[1], x.split(",")[0])) # [(date, name)]
    worker_grouped = worker_split.reduceByKey(lambda a, b: a + "," + b) # [(date, 'name,name,name')]
    worker_paired =  worker_grouped.flatMap(pair) # [(('name', 'name'), 1)]
    worker_paired = worker_paired.reduceByKey(lambda a, b: a+b) # [(('name', 'name'), int)]
    worker_paired_sorted = worker_paired.sortBy(lambda x: x[1], ascending=False)
    # print(worker_paired_sorted.collect())
    return worker_paired_sorted


def air_flights_most_canceled_flights(flights: DataFrame) -> str:
    """
    Takes the flight data as a DataFrame and finds the airline that had the most canceled flights on Sep. 2021
    :param flights: Spark DataFrame of the flights CSV file.
    :return: The name of the airline with most canceled flights on Sep. 2021.
    """
    flights = flights.filter((flights.Year == 2021) & (flights.Month == 9) & (flights.Cancelled))
    flights = flights.groupBy("Airline").count()
    # flights.show()
    most_canceled = flights.agg({"count": "max"}).collect()[0][0]
    # print(most_canceled)
    return flights.filter(col("count") == most_canceled).select("Airline").collect()[0][0]


def air_flights_diverted_flights(flights: DataFrame) -> int:
    """
    Takes the flight data as a DataFrame and calculates the number of flights that were diverted in the period of 
    20-30 Nov. 2021.
    :param flights: Spark DataFrame of the flights CSV file.
    :return: The number of diverted flights between 20-30 Nov. 2021.
    """
    return flights.filter((flights.Year == 2021) & (flights.Month == 11) & (flights.DayofMonth >= 20) & (flights.DayofMonth <= 30) & (flights.Diverted)).count()


def air_flights_avg_airtime(flights: DataFrame) -> float:
    """
    Takes the flight data as a DataFrame and calculates the average airtime of the flights from Nashville, TN to 
    Chicago, IL.
    :param flights: Spark DataFrame of the flights CSV file.
    :return: The average airtime average airtime of the flights from Nashville, TN to 
    Chicago, IL.
    """
    return flights.filter((flights.OriginCityName == 'Nashville, TN') & (flights.DestCityName == 'Chicago, IL')).agg({"AirTime": "avg"}).collect()[0][0]


def air_flights_missing_departure_time(flights: DataFrame) -> int:
    """
    Takes the flight data as a DataFrame and find the number of unique dates where the departure time (DepTime) is 
    missing.
    :param flights: Spark DataFrame of the flights CSV file.
    :return: the number of unique dates where DepTime is missing. 
    """
    return flights.where(col('DepTime').isNull()).select('FlightDate').distinct().count()



def main():
    # initialize SparkContext and SparkSession
    sc = SparkContext('local[*]')
    spark = SparkSession.builder.getOrCreate()

    print('########################## Problem 1 ########################')
    # problem 1: restaurant shift coworkers with Spark and MapReduce 
    # read the file
    worker_shifts = sc.textFile('worker_shifts.txt')
    sorted_num_coworking_shifts = restaurant_shift_coworkers(worker_shifts)
    # print the most, least, and average number of shifts together
    sorted_num_coworking_shifts.persist()
    print('Co-Workers with most shifts together:', sorted_num_coworking_shifts.first())
    print('Co-Workers with least shifts together:', sorted_num_coworking_shifts.sortBy(lambda x: (x[1], x[0])).first())
    print('Avg. No. of Shared Shifts:',
          sorted_num_coworking_shifts.map(lambda x: x[1]).reduce(lambda x,y: x+y)/sorted_num_coworking_shifts.count())
    
    print('########################## Problem 2 ########################')
    # problem 2: PySpark DataFrame operations
    # read the file
    flights = spark.read.csv('Combined_Flights_2021_small.csv', header=True, inferSchema=True)
    print('Q1:', air_flights_most_canceled_flights(flights), 'had the most canceled flights in September 2021.')
    print('Q2:', air_flights_diverted_flights(flights), 'flights were diverted between the period of 20th-30th '
                                                       'November 2021.')
    print('Q3:', air_flights_avg_airtime(flights), 'is the average airtime for flights that were flying from '
                                                   'Nashville to Chicago.')
    print('Q4:', air_flights_missing_departure_time(flights), 'unique dates where departure time (DepTime) was '
                                                              'not recorded.')
    

if __name__ == '__main__':
    main()
