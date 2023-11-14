# Databricks notebook source
code1_table_name = dbutils.jobs.taskValues.get(taskKey    = "setup_test", \
                            key        = "code1_table_name", \
                            default    = "my_data", \
                            debugValue = "table_name")

code1_filtered_name = dbutils.jobs.taskValues.get(taskKey    = "setup_test", \
                            key        = "code1_filtered_name", \
                            default    = "code1_filtered_name", \
                            debugValue = "table_name_filter")

code1_filter = dbutils.jobs.taskValues.get(taskKey    = "setup_test", \
                            key        = "code1_filter", \
                            default    = 5, \
                            debugValue = 1)

# COMMAND ----------

spark.sql(f"CREATE OR REPLACE TABLE {code1_filtered_name} as SELECT * FROM {code1_table_name} WHERE id > {code1_filter}")

# COMMAND ----------

spark.sql(f"select * from {code1_filtered_name}").display()
