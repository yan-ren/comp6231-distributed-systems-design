from pyspark import SparkContext
sc = SparkContext("local[*]")

receipt = sc.textFile('receipt.txt')
receipt_mapped = receipt.map(lambda x: float(x.split()[1]))
revenue = receipt_mapped.reduce(lambda x, y: x+y)

print(revenue)

