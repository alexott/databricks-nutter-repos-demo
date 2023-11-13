# Databricks notebook source
# MAGIC %run ../Code1

# COMMAND ----------

# MAGIC %run ../Code2

# COMMAND ----------

print("Running Code 1..")
generate_data1()

print("Running Code 2..")
generate_data2()

# COMMAND ----------

# MAGIC %sql
# MAGIC select *
# MAGIC from my_data

# COMMAND ----------

# MAGIC %sql
# MAGIC select *
# MAGIC from my_data

# COMMAND ----------

# MAGIC %sql
# MAGIC select * from my_data where id > 5
