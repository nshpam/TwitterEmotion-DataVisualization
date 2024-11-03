# dataset configs
FILE_NAME = 'train-00000-of-00001.parquet'
# LABEL = 5
LABEL = 0
TOP = 100
TEXT_FIELD = {'_id': 0, 'label':0}

# mongo configs
MONGO_CLIENT = 'mongodb://localhost:27017/'
MONGO_DB = 'TwitterEmotion'
MONGO_COLLECTION = 'Raw'