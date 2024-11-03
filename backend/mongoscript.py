from pymongo import MongoClient
import pandas as pd
import config

df_parquet = pd.read_parquet(config.FILE_NAME) # read data from parquet file
data = df_parquet.to_dict(orient='records') # convert to dict

# connect to mongodb
client = MongoClient(config.MONGO_CLIENT)
db = client[config.MONGO_DB]
col = db[config.MONGO_COLLECTION] 

# insert data from parquet into mongodb database
col.insert_many(data)
