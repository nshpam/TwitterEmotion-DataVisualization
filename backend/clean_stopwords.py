import pandas as pd
import config
import nltk
import mongoscript
# nltk.download('stopwords') # for first time
# nltk.download('opinion_lexicon') # for first time
from nltk.corpus import stopwords
# from nltk.corpus import opinion_lexicon # sentiment library

# connect to mongodb
col = mongoscript.connect_collection(config.MONGO_COLLECTION_1)

# query data by label
def query_label(label, limit):
    if limit:
       return list(col.find({'label': label}, {'_id': 0, 'label':0}).limit(100))
    
    return list(col.find({'label': label}, {'_id': 0, 'label':0}))

filter_record = {}
count_sentence = {}
clean_stop = []

def filter_data(raw, data, label):
    new_list = []
    stop_words = set(stopwords.words('english'))
    # positive = set(opinion_lexicon.positive())
    # negative = set(opinion_lexicon.negative())

    for word in data:

        # remove stop words
        if word in stop_words: 
            if word not in filter_record:
                filter_record[word] = 1
            else:
                filter_record[word] += 1
        else:
            new_list.append(word)

    clean_stop.append({
        'text' : raw,
        'clean' : new_list,
        'label' : label
    })

        # print(word)
    return new_list

def get_top(top_num):

    sort_record = {}
    sorted_filter_record= dict(sorted(filter_record.items(), key=lambda item: item[1], reverse=True))

    for record in sorted_filter_record.items():
        count = list(record)[1]
        word = list(record)[0]

        if count not in sort_record:
            sort_record[count] = [word]
        else:
            sort_record[count].append(word)

    count_keys = sorted(sort_record.items(), reverse=True)[:top_num]

    return count_keys


for num in range(config.LABEL+1):
    all_list = []
    # print(num , len(query_label(num, False)))
    documents = query_label(num, False)
    raw_list = [doc['text'] for doc in documents]
    for raw in raw_list:
        filtered_data = filter_data(raw, raw.split(' '), num)
        all_list.append(filtered_data)

# print(clean_stop)
mongoscript.dump_mongodb(clean_stop, mongoscript.connect_collection(config.MONGO_COLLECTION_2))

# print(filter_record)

df = pd.DataFrame(get_top(config.TOP))
print(df)
