from pyspark.sql import SparkSession

# initialize Spark
spark = SparkSession.builder.getOrCreate()
# read the CSV file
titanic = spark.read.csv('titanic.csv', header=True, inferSchema=True)

# Ex 1:
# method 1:
print(titanic.agg({'Age': 'min'}).collect())

# method 2:
from pyspark.sql.functions import min
print(titanic.select(min('Age')).collect())


# Ex 2:
print('Duplicate Names?:', titanic.count() == titanic.select('Name').distinct().count())


# Ex 3:
print('Unique ticket prices:', titanic.select('Fare').distinct().count())


# Ex 4:
print('Correlation Age-Survived:', titanic.stat.corr('Survived', 'Age'))

# Ex5:
print('Avg. Age:')
titanic.groupBy('Sex').avg('Age').show()

# Ex 6:
from pyspark.sql.functions import col, udf
from pyspark.sql.types import StringType
step_udf = udf(lambda x: 'unknown' if not x else '1-20' if x < 20 else '20-40' if x >= 20 and x < 40 else '40+', StringType())
titanic_with_age_groups = titanic.withColumn('AgeGroup', step_udf(col('Age')))
num_survived_per_age_group = titanic_with_age_groups.groupBy('AgeGroup').avg('Survived')
num_survived_per_age_group = num_survived_per_age_group.orderBy('avg(Survived)')
num_survived_per_age_group.show()
