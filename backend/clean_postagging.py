import pandas as pd
import config
import nltk
# nltk.download('averaged_perceptron_tagger_eng') # for first time
from nltk import pos_tag
from nltk.corpus import wordnet
import mongoscript

# connect to mongodb
col = mongoscript.connect_collection(config.MONGO_COLLECTION_2)

# query data by label
def query_label(label, limit):
    if limit:
       return list(col.find({'label': label}, {'_id': 0, 'label':0}).limit(100))
    
    return list(col.find({'label': label}, {'_id': 0, 'label':0}))

filter_record = []

def get_wordnet_pos(treebank_tag):
    if treebank_tag.startswith('J'):
         return wordnet.ADJ
    elif treebank_tag.startswith('V'):
        return wordnet.VERB
    elif treebank_tag.startswith('N'):
        return wordnet.NOUN
    elif treebank_tag.startswith('R'):
        return wordnet.ADV
    else:
        return wordnet.NOUN  # Default to noun

def pos_tagging(raw, data, label):
    tagged_data = pos_tag(data)
    tagged_data = [[token, get_wordnet_pos(tag)] for token, tag in tagged_data]

    filter_record.append({
        'text' : raw,
        'clean' : tagged_data,
        'label' : label
    })

    return tagged_data

count_sentence = {}
clean_stop = []

for num in range(config.LABEL+1):
    documents = query_label(num, False)
    raw_list = [doc for doc in documents]

    for raw in raw_list:
        pos_tagging(raw['text'], raw['clean'], num)

# print(filter_record)
mongoscript.dump_mongodb(filter_record, mongoscript.connect_collection(config.MONGO_COLLECTION_3))
