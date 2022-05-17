# Databricks notebook source
#jake test
def generate_data2(table_name="my_data"):
  df = spark.range(0,10)
  df.write.format("delta").mode("overwrite").saveAsTable(table_name)
