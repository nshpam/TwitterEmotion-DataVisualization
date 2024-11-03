import pandas as pd
import config
import nltk
import mongoscript
from nltk.corpus import names
# nltk.download('names') # for first time

male_names = names.words('male.txt')
female_names = names.words('female.txt')

male_list = []
female_list = []

# connect to mongodb
col = mongoscript.connect_collection(config.MONGO_COLLECTION_3)

filter_list=['Love','Wake','Way','See','Rice','Case','Job','Chance','Wait','Glad','Saw','Trip','Hope','Pet','Star','Lion','Say'
             ,'Honor','Patience','Web','Dot','Forest','Hall','Town','Fan','Waiter','Pace','Tuesday','Row','Deny','Bird','Wash'
             ,'Win','Dusty','Shadow','Skip','Fox','Worth']
possesive_noun_male=['He','His','Guy']
possesive_noun_female=['She','Her','Hers']

# query data by label
def query_label(label, limit):
    if limit:
       return list(col.find({'label': label}, {'_id': 0, 'label':0}).limit(100))
    
    return list(col.find({'label': label}, {'_id': 0, 'label':0}))

def check_name_gender(name):

    name = name.capitalize()  # Capitalize the name to match corpus format

    if name in filter_list:
        return "Unknown"
    if name in possesive_noun_male:
        return "Male"
    elif name in possesive_noun_female:
        return "Female"
    elif name in male_names and name in female_names:
        return "Ambiguous" # could be either male or female
    elif name in male_names:
        return "Male"
    elif name in female_names:
        return "Female"
    else:
        return "Unknown"
    
all_data = []

for num in range(config.LABEL+1):
    all_list = []
    # print(num , len(query_label(num, False)))
    documents = query_label(num, False)
    raw_list = [doc for doc in documents]
    for raw in raw_list:
        # print(raw)
        gender_list = {"Female":[], "Male":[]}
        for item in raw['clean']:
            word = item[0]
            if item[1] != 'n':
                continue
            gender = check_name_gender(word)
            if gender in ["Unknown", "Ambiguous"]:
                continue
            
            if word not in gender_list[gender]:
                gender_list[gender].append(word)
            
        if gender_list['Female']!=[] or gender_list['Male']!=[]:
            all_data.append({
                'text' : raw['text'],
                'Female' : gender_list['Female'],
                'Male' : gender_list['Male'],
                'label' : num
            })

mongoscript.dump_mongodb(all_data, mongoscript.connect_collection(config.MONGO_COLLECTION_5))
# print(all_data)
# df = pd.DataFrame(all_data)
# df.to_csv('gender_2.csv', index=False)

# print(df)