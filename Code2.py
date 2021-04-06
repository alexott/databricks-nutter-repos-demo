# Databricks notebook source
def generate_data():
  df = spark.range(0,10)
  df.write.format("delta").mode("overwrite").saveAsTable("my_data")

# COMMAND ----------

generate_data()

# COMMAND ----------

# another release trigger
# one more change
