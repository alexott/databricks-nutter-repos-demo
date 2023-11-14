# Databricks notebook source
from pyspark.sql.types import StructType,StructField,LongType

# COMMAND ----------

code1_table_name = dbutils.jobs.taskValues.get(taskKey    = "run_integration_test", \
                            key        = "code1_table_name", \
                            default    = "my_data", \
                            debugValue = "table_name")

code1_filtered_name = dbutils.jobs.taskValues.get(taskKey    = "run_integration_test", \
                            key        = "code1_filtered_name", \
                            default    = "code1_filtered_name", \
                            debugValue = "table_name_filter")


# COMMAND ----------

df = spark.read.table(f"{code1_filtered_name}")
assert df.count() == 4

# COMMAND ----------

table_schema = StructType([StructField('id', LongType(), True)])
df_schema = spark.read.table(f"{code1_table_name}").schema
assert df_schema == table_schema

# COMMAND ----------

#drop table after test
spark.sql(f"drop table {code1_filtered_name}")
