import pandas as pd
import config
import mongoscript

col = mongoscript.connect_collection(config.MONGO_COLLECTION_5)

def query_label(label, limit):
    if limit:
       return list(col.find({'label': label}, {'_id': 0, 'label':0}).limit(100))
    
    return list(col.find({'label': label}, {'_id': 0, 'label':0}))

for num in range(config.LABEL+1):
    all_list = {'Female':[],'Male':[]}
    # print(num , len(query_label(num, False)))
    documents = query_label(num, False)
    raw_list_female = [doc['Female'] for doc in documents]
    for raw in raw_list_female:
        if raw == []:
            continue
        all_list['Female']+=raw
        # Male
        # if raw['Male'] != []:

        # Female

print(all_list)
