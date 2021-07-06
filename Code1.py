# Databricks notebook source
def generate_data1(n=1000, name='my_cool_data'):
  df = spark.range(0, n)
  df.createOrReplaceTempView(name)

# COMMAND ----------

# trigger release pipeline 

# COMMAND ----------

# just a change of the code to trigger release
