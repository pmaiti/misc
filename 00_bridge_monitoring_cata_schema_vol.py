# Databricks notebook source
ext_loc = "abfss://databricks@samighty01.dfs.core.windows.net/bridge_monitoring"

spark.sql(
    f"""
    CREATE CATALOG IF NOT EXISTS bridge_monitoring
    MANAGED LOCATION '{ext_loc}'
    """
)

# COMMAND ----------

try:
    spark.sql("create schema bridge_monitoring.00_landing;")
except:
    print('check if 00_landing schema already exists')

try:
    spark.sql("create schema bridge_monitoring.01_bronze;")
except:
    print('check if 01_bronze schema already exists')

try:
    spark.sql("create schema bridge_monitoring.02_silver;")
except:
    print('check if 02_silver schema already exists')

try:
    spark.sql("create schema bridge_monitoring.03_gold;")
except:
    print('check if 03_gold schema already exists')

# COMMAND ----------

# Create the volume 'streaming' under the bridge_monitoring.00_landing schema
spark.sql("""
    CREATE VOLUME IF NOT EXISTS bridge_monitoring.00_landing.streaming
""")

# Create 3 folders under the 'streaming' volume
dbutils.fs.mkdirs("/Volumes/bridge_monitoring/00_landing/streaming/bridge_temperature")
dbutils.fs.mkdirs("/Volumes/bridge_monitoring/00_landing/streaming/bridge_tilt")
dbutils.fs.mkdirs("/Volumes/bridge_monitoring/00_landing/streaming/bridge_vibration")

# COMMAND ----------

# Read data from Delta tables in the three folders under the streaming volume

df_temperature = spark.read.format("delta").load("/Volumes/bridge_monitoring/00_landing/streaming/bridge_temperature")
df_tilt = spark.read.format("delta").load("/Volumes/bridge_monitoring/00_landing/streaming/bridge_tilt")
df_vibration = spark.read.format("delta").load("/Volumes/bridge_monitoring/00_landing/streaming/bridge_vibration")

display(df_temperature)
display(df_tilt)
display(df_vibration)

# COMMAND ----------

# MAGIC %sql
# MAGIC select * from delta.`/Volumes/bridge_monitoring/00_landing/streaming/bridge_temperature/`;
# MAGIC select * from delta.`/Volumes/bridge_monitoring/00_landing/streaming/bridge_tilt/`;
# MAGIC select * from delta.`/Volumes/bridge_monitoring/00_landing/streaming/bridge_vibration/`;