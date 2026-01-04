from pyspark.sql import SparkSession
from pyspark.sql.types import IntegerType,StringType,StructField,StructType,ArrayType,FloatType
from pyspark.sql.functions import from_json,col,explode,md5,concat_ws

def read_topic(topic,schema):
    df = spark.readStream\
         .format("kafka")\
         .option("kafka.bootstrap.servers","localhost:9092")\
         .option("subscribe",topic)\
         .option("startingOffsets","earliest")\
         .load()


    df = df.selectExpr("CAST(value AS STRING)")
    data = df.select(from_json(col("value").cast("string"),ArrayType(schema)).alias("payload"))
    exp = data.filter(col("payload").isNotNull())\
            .select(explode("payload").alias("record"))
    
    return exp.select("record.*")



spark = SparkSession.builder\
        .appName("KafkaConsumer")\
        .config("spark.jars.packages","org.apache.spark:spark-sql-kafka-0-10_2.13:4.1.0")\
        .getOrCreate()

schema1 = StructType([
    StructField("rowID",IntegerType(),True),
    StructField("Model",StringType(),True),
    StructField("Year",IntegerType(),True),
    StructField("Color",StringType(),True)
])

schema2 = StructType([
    StructField("rowID",IntegerType(),True),
    StructField("Fuel_Type",StringType(),True),
    StructField("Transmission",StringType(),True),
    StructField("Engine_Size_L",FloatType(),True),
    StructField("Mileage_KM",IntegerType(),True)
])

schema3 = StructType([
    StructField("rowID",IntegerType(),True),
    StructField("Region",StringType(),True),
    StructField("Price_USD",IntegerType(),True),
    StructField("Sales_Volume",IntegerType(),True),
    StructField("Sales_Classification",StringType(),True),
])

model = read_topic("bmw_model",schema1)
info = read_topic("bmw_info",schema2)
sales = read_topic("bmw_sales",schema3)

#hna ghadi ndir creation ldim tables and fact table:)
car_dim = model.join(info,"rowID")\
        .select("Model","Year","Color","Fuel_Type","Transmission","Engine_Size_L")\
        .distinct()\
        .withColumn("car_key",md5(concat_ws("||","Model","Year","Fuel_Type","Engine_Size_L","Transmission","color")))

junk_dim = sales.select("Region","Sales_Classification")\
        .distinct()\
        .withColumn("junk_key",md5(concat_ws("||","Sales_Classification","Region")))

fact_tab = sales.join(model,"rowID").join(info,"rowID")\
        .join(car_dim,["Model","Year","Color","Fuel_Type","Transmission","Engine_Size_L"])\
        .join(junk_dim,["Region","Sales_Classification"])\
        .select(
            col("rowID").alias("transaction_id"),
            "car_key",
            "junk_key",
            "Price_USD",
            "Sales_Volume",
            "Mileage_KM"
        )

query = car_dim.writeStream\
        .outputMode("append")\
        .format("console")\
        .start()

query.awaitTermination()

