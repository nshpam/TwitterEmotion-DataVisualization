import mongoscript
import config
import pandas as pd

# prepare data
print('----------START----------')
print('IMPORT FILE ',config.FILE_NAME)
df_parquet = pd.read_parquet(config.FILE_NAME) # read data from parquet file
data = df_parquet.to_dict(orient='records') # convert to dict

# dump file
print(f'DUMP FILE {config.FILE_NAME} TO {config.MONGO_COLLECTION_1} > {config.MONGO_DB}')
mongoscript.dump_mongodb(data, mongoscript.connect_collection(config.MONGO_COLLECTION_1))
print('----------FINISH----------')