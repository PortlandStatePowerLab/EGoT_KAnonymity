from spark_privacy_preserver.mondrian_preserver import Preserver #requires pandas


print('got here!')
data = [
    [0,'a1','b1','d2'],
    [1,'a1','b1','d2'],
    [2,'a1','b1','d2'],
]
# schema = StructType([
#     StructField('index',IntegerType()),
#     StructField('col1',StringType()),
#     StructField('col2',StringType()),
#     StructField('col3',StringType()),
# ])
sensitive_col = 'col3'

# df = spark.createDataFrame(data,schema=schema)
# print(df)
print('done')