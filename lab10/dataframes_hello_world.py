from pyspark.sql import SparkSession

# initialize Spark
spark = SparkSession.builder.getOrCreate()
# read the CSV file
titanic = spark.read.csv('titanic.csv', header=True, inferSchema=True)
# print the schema
titanic.printSchema()
# print a few rows
titanic.show()

print('Number of rows in dataset:', titanic.count())
print('Number of rows without NaNs:', titanic.dropna().count())

# # filtration & selection
survived = titanic.filter((titanic.Survived == 1) & (titanic.Age > 60))
survived_names_and_ages = survived.select('Name', 'Age')
rows = survived_names_and_ages.collect()

print(rows[0].Age)
