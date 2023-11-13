# Databricks notebook source
# MAGIC %run ../../pipeline/demo_pipeline

# COMMAND ----------


dbutils.jobs.taskValues.set(key    = "code1_table_name", \
                            value = "my_data")

dbutils.jobs.taskValues.set(key   = "code1_filter_name", \
                            value = "my_data_filtered")

dbutils.jobs.taskValues.set(key   = "code1_filter", \
                            value = 5)
