import pandas as pd
import config
import mongoscript
import re

col = mongoscript.connect_collection(config.MONGO_COLLECTION_5)

def query_label(label, limit):
    if limit:
       return list(col.find({'label': label}, {'_id': 0, 'label':0}).limit(100))
    
    return list(col.find({'label': label}, {'_id': 0, 'label':0}))

for num in range(config.LABEL+1):
    all_list_count = {'Female':{},'Male':{}}
    all_list_female = {}
    all_list_male = {}
    # print(num , len(query_label(num, False)))
    documents = query_label(num, False)

    # Female
    raw_list_female = [doc for doc in documents]
    for raw in raw_list_female:
        if raw['Female'] == []:
            continue
        for name in raw['Female']:
            # count
            if name not in all_list_count['Female']:
                all_list_count['Female'][name] = 1
                
            else:
                all_list_count['Female'][name] += 1
            
            # text
            if name not in all_list_female:
                all_list_female[name] = [raw['text']]
            else:
                all_list_female[name].append(raw['text'])

    # Male
    raw_list_male = [doc for doc in documents]
    for raw in raw_list_male:
        for name in raw['Male']:
            # count
            if name not in all_list_count['Male']:
                all_list_count['Male'][name] = 1
                
            else:
                all_list_count['Male'][name] += 1
            
            # text
            if name not in all_list_male:
                all_list_male[name] = [raw['text']]
            else:
                all_list_male[name].append(raw['text'])
        
    sorted_female= dict(sorted(all_list_count['Female'].items(), key=lambda item: item[1], reverse=True))
    sorted_male= dict(sorted(all_list_count['Male'].items(), key=lambda item: item[1], reverse=True))

print(sorted_female)
# print(all_list_female['joy'])
print(sorted_male)
# print(all_list_male['art'])

# pattern = [r'\bsome may\b',r'\bi may\b',r'\bthis may\b',r'\byou may\b',r'\bin may\b',r'\bhe may\b',r'\bit may\b',r'\bthere may\b'
#            ,r'\bmay be\b',r'\bwho may\b',r'\bmay have\b',r'\bwhich may\b',r'\bnext may\b',r'\bthat may\b',r'\bthey may\b']
# count = 0
# count_main = 0

# for text in all_list_male['lay']:
#     highlighted_text = re.sub(r'\b(lay)\b', r'**\1**', text)
#     print(highlighted_text)

# for text in all_list_female['may']:

#     count_main+=1

#     filter_text = text
    
#     for p in pattern:
#         if re.search(p, text):
#             filter_text = re.sub(r'\bmay\b', ' ', text)

#     if re.search(r'\bmay\b', filter_text):
#         print(filter_text)
#         count+=1
    
# print('before',count_main,'after',count)
