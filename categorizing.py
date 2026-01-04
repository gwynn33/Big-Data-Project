import pandas as pd 
from kafka import KafkaProducer


def slicer(dataset,producer,topic_name,chunk_size=2000):
    for start in range(0,len(dataset),chunk_size):
        subset = dataset[start:start+chunk_size]
        subset_to_json = subset.to_json(orient="records")
        try:
            producer.send(topic_name,subset_to_json.encode("utf-8"))
        except Exception as e:
            print(f"There is an Error while trying to send the chunk ({start},{start+chunk_size}) : {e}")

#hna drt lcategorizing ldata cuz i want to pass it through my topics 
df = pd.read_csv('BMW sales data (2010-2024) (1) (1).csv')

"""-------------------------------------------------------
    (bmw_model,bmw_info,bmw_sales) is large blob json data =>
    which means (json_file > producers_limits = 1mb)
-------------------------------------------------------
"""
try:
    producer = KafkaProducer(bootstrap_servers='localhost:9092')
except Exception as e: 
    print(f"Failed To Connect To Kafka : {e}")

bmw_model = df[['Model','Year','Color']]
bmw_info = df[['Fuel_Type','Transmission','Engine_Size_L','Mileage_KM']]
bmw_sales = df[['Region','Price_USD','Sales_Volume','Sales_Classification']]
#hna ghadi ndir reset l index bach mant7nsroch f spark
bmw_model = bmw_model.reset_index().rename(columns={"index":"rowID"})
bmw_info = bmw_info.reset_index().rename(columns={"index":"rowID"})
bmw_sales = bmw_sales.reset_index().rename(columns={"index":"rowID"})

slicer(bmw_model,producer,"bmw_model")
slicer(bmw_info,producer,"bmw_info")
slicer(bmw_sales,producer,"bmw_sales")

producer.flush()
producer.close()
