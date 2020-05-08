import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from gensim.models import TfidfModel
from gensim.corpora.dictionary import Dictionary
from operator import itemgetter

sns.set_color_codes()

# Load data and make each document a day's briefing 
df = pd.read_csv('../../../data/processed/trump_wh_remarks.csv')
df = df.drop(columns=['text','normalized_text'])
df = df.groupby(['date'])['clean_text'].apply(' '.join).reset_index()
remarks = [i.split() for i in list(df['clean_text'].values)]

# Create and fit model to each statement
common_dictionary = Dictionary(remarks)
common_corpus = [common_dictionary.doc2bow(remark) for remark in remarks] # corpus to BoW
model = TfidfModel(common_corpus,id2word=common_dictionary)  # fit model

# Now get topics by briefing date
corpus_tfidf = model[common_corpus]
briefing_keywords = []
num_words = 6 # how many keywords we want to extract per date
for row,doc in enumerate(corpus_tfidf):
    d=[]
    for idx, value in doc:
        word = common_dictionary.get(idx)
        score = value
        d.append((word, score))

    e=sorted(d, key=itemgetter(1))
    top = e[-num_words:][::-1]
    date = df.loc[[row]].date.values[0]
    #print(["%s, %.2f" % item for item in top])
    words = ["%s" % item[0] for item in top]
    briefing_keywords.append([date] + words)

keywords = pd.DataFrame(briefing_keywords,columns=['Date']+["Keyword "+str(word+1) for word in range(num_words)])
keywords = keywords.set_index('Date')
keywords.to_csv('keywords.csv')

