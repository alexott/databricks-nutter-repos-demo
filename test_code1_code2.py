# Databricks notebook source
# install nutter in cluster if you want to trigger tests from command line
%python
%pip install -U nutter

# COMMAND ----------

from runtime.nutterfixture import NutterFixture, tag

default_timeout = 600

class Test1Fixture(NutterFixture):
  def __init__(self):
    self.code1_result = ''
    self.code2_table_name = "my_data"
    NutterFixture.__init__(self)
    
  def run_name1(self):
    self.code1_result = dbutils.notebook.run('./Code1', default_timeout, {'name': 'world'})
    
  def assertion_name1(self):
    assert(self.code1_result == "Hello world")

  def run_name2(self):
    self.code1_result = dbutils.notebook.run('./Code1', default_timeout)

  def assertion_name2(self):
    assert(self.code1_result == "ERROR")

  def run_code2(self):
    # if we use `dbutils.notebook.run`, then we need to call `generate_data()` from inside of it...
    # in that case we may need to have a separate notebook that will load functions & call that function
    dbutils.notebook.run('./Code2', default_timeout)
    
  def assertion_code2(self):
    some_tbl = sqlContext.sql(f'SELECT COUNT(*) AS total FROM {self.code2_table_name}')
    first_row = some_tbl.first()
    assert (first_row[0] == 10)

  def after_code2(self):
    spark.sql(f"drop table {self.code2_table_name}")

# COMMAND ----------

result = Test1Fixture().execute_tests()
print(result.to_string())
# Comment out the next line (result.exit(dbutils)) to see the test result report from within the notebook
is_job = dbutils.notebook.entry_point.getDbutils().notebook().getContext().currentRunId().isDefined()
if is_job:
  result.exit(dbutils)