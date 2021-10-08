# Databricks notebook source
# MAGIC %pip install -U nutter chispa

# COMMAND ----------

# MAGIC %run ./Code1

# COMMAND ----------

# MAGIC %run ./Code2

# COMMAND ----------

# https://github.com/microsoft/nutter
from runtime.nutterfixture import NutterFixture, tag
# https://github.com/MrPowers/chispa
from chispa.dataframe_comparer import *

class Test1Fixture(NutterFixture):
  def __init__(self):
    self.code2_table_name = "my_data"
    self.code1_view_name = "my_cool_data"
    self.code1_num_entries = 100
    NutterFixture.__init__(self)
    
  def run_code1(self):
    generate_data1(n = self.code1_num_entries, name = self.code1_view_name)
    
  def assertion_code1(self):
    df = spark.read.table(self.code1_view_name)
    assert(df.count() == self.code1_num_entries)
    
  def run_code2(self):
    generate_data2(table_name = self.code2_table_name)
    
  def assertion_code2(self):
    some_tbl = sqlContext.sql(f'SELECT COUNT(*) AS total FROM {self.code2_table_name}')
    first_row = some_tbl.first()
    assert (first_row[0] == 10)

  def after_code2(self):
    spark.sql(f"drop table {self.code2_table_name}")
    
  # we're using Chispa library here to compare the content of the processed dataframe with expected results
  def assertion_upper_columns(self):
    cols = ["col1", "col2", "col3"]
    df = spark.createDataFrame([("abc", "cef", 1)], cols)
    upper_df = upper_columns(df, cols)
    expected_df = spark.createDataFrame([("ABC", "CEF", 1)], cols)
    assert_df_equality(upper_df, expected_df)

# COMMAND ----------

result = Test1Fixture().execute_tests()
print(result.to_string())
is_job = dbutils.notebook.entry_point.getDbutils().notebook().getContext().currentRunId().isDefined()
if is_job:
  result.exit(dbutils)

# COMMAND ----------

# Test Comment
