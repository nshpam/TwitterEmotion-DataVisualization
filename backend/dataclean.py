from pymongo import MongoClient
import pandas as pd
import config
import nltk
# nltk.download('stopwords')
# nltk.download('opinion_lexicon')
from nltk.corpus import stopwords
from nltk.corpus import opinion_lexicon # sentiment library

# connect to mongodb
client = MongoClient(config.MONGO_CLIENT)
db = client[config.MONGO_DB]
col = db[config.MONGO_COLLECTION] 

# query data by label
def query_label(label, limit):
    if limit:
       return list(col.find({'label': label}, {'_id': 0, 'label':0}).limit(100))
    
    return list(col.find({'label': label}, {'_id': 0, 'label':0}))

filter_record = {'stopword':{}}
count_sentence = {}

def filter_data(data):
    new_list = []
    stop_words = set(stopwords.words('english'))
    positive = set(opinion_lexicon.positive())

    for word in data:

        removed = False

        # remove stop words
        if word in stop_words: 
            if word not in filter_record['stopword']:
                filter_record['stopword'][word] = 1
            else:
                filter_record['stopword'][word] += 1
            removed = True
        
        if word in positive:
            print(word)

        if not removed:
            new_list.append(word)
        # print(word)
    return new_list

def get_top(top_num, field):

    sort_record = {}
    sorted_filter_record= dict(sorted(filter_record[field].items(), key=lambda item: item[1], reverse=True))

    for record in sorted_filter_record.items():
        count = list(record)[1]
        word = list(record)[0]

        if count not in sort_record:
            sort_record[count] = [word]
        else:
            sort_record[count].append(word)

    count_keys = sorted(sort_record.items(), reverse=True)[:top_num]

    return count_keys
    # return sorted_word_counts

for num in range(config.LABEL+1):
    # print(num , len(query_label(num, False)))
    documents = query_label(num, True)
    raw_list = [doc['text'] for doc in documents]
    all_list = []

    for raw in raw_list:
        filtered_data = filter_data(raw.split(' '))
        # if 'because' in raw or 'think' in raw:
        # if 'i ' in raw:
            # because.append(raw)
        all_list.append(filtered_data)
    
    # print(all_list)
    # print(because)

print(filter_record)

df = pd.DataFrame(get_top(config.TOP, 'stopword'))
print(df)
