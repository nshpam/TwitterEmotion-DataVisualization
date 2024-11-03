from pymongo import MongoClient
import pandas as pd

df_parquet = pd.read_parquet('train-00000-of-00001.parquet') # read data from parquet file
data = df_parquet.to_dict(orient='records') # convert to dict

# connect to mongodb
client = MongoClient("mongodb://localhost:27017/")
db = client['TwitterEmotion']
col = db["Raw"] 

# insert data from parquet into mongodb database
col.insert_many(data)
