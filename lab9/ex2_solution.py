from pyspark import SparkContext
sc = SparkContext("local[*]")

students = sc.textFile('students.txt')
students_mapped = students.flatMap(lambda x: [(i, 1) for i in x.split()[1:]])
course_students = students_mapped.reduceByKey(lambda x, y: x+y)

course_students_sorted = course_students.sortBy(lambda x: x[1], ascending=False)
print(course_students_sorted.collect())
