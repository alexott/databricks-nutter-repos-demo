# Databricks notebook source
# MAGIC %pip install -U nutter

# COMMAND ----------

# MAGIC %run ./Code1

# COMMAND ----------

# MAGIC %run ./Code2

# COMMAND ----------

from runtime.nutterfixture import NutterFixture, tag

class Test1Fixture(NutterFixture):
  def __init__(self):
    self.code2_table_name = "my_data"
    self.code1_view_name = "my_cool_data"
    self.code1_num_entries = 100
    NutterFixture.__init__(self)
    
  def run_name1(self):
    generate_data1(n = self.code1_num_entries, name = self.code1_view_name)
    
  def assertion_name1(self):
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

# COMMAND ----------

result = Test1Fixture().execute_tests()
print(result.to_string())
is_job = dbutils.notebook.entry_point.getDbutils().notebook().getContext().currentRunId().isDefined()
if is_job:
  result.exit(dbutils)

# COMMAND ----------


