# Databricks notebook source
import pyspark.sql.functions as F
import pyspark.sql.types as T
from pyspark.sql import DataFrame, SparkSession

# COMMAND ----------

def generate_data1(n=1000, name='my_cool_data'):
    df = SparkSession.getActiveSession().range(0, n)
    df.createOrReplaceTempView(name)

# COMMAND ----------

def upper_columns(df: DataFrame, cols: list) -> DataFrame:
    new_cols = []
    for field in df.schema.fields:
        if field.dataType == T.StringType() and field.name in cols:
            new_cols.append(F.upper(F.col(field.name)).alias(field.name))
        else:
            new_cols.append(F.col(field.name))
            
    return df.select(*new_cols)
