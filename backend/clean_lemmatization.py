import pandas as pd
import config
import nltk
# nltk.download('wordnet') # for first time
from nltk.stem import WordNetLemmatizer
import mongoscript

# connect to mongodb
col = mongoscript.connect_collection(config.MONGO_COLLECTION_3)

# query data by label
def query_label(label, limit):
    if limit:
       return list(col.find({'label': label}, {'_id': 0, 'label':0}).limit(100))
    
    return list(col.find({'label': label}, {'_id': 0, 'label':0}))

filter_record = []
lemmatizer = WordNetLemmatizer()

def lemma_data(raw, data, label):

    lemmatized_words = []
    for item in data:

        lemmatized_words.append(lemmatizer.lemmatize(item[0], pos=item[1]))
        
    filter_record.append({
        'text' : raw,
        'clean' : lemmatized_words,
        'label' : label
    })

    return lemmatized_words

# count_sentence = {}
# clean_stop = []

for num in range(config.LABEL+1):
    documents = query_label(num, False)
    raw_list = [doc for doc in documents]

    for raw in raw_list:
        lemma_data(raw['text'], raw['clean'], num)

# print(filter_record)
mongoscript.dump_mongodb(filter_record, mongoscript.connect_collection(config.MONGO_COLLECTION_4))
