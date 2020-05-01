import glob
import nltk
from clean_text import normalize 
from collections import Counter
from gensim.models import Phrases
from gensim.models.phrases import Phraser
from nltk.corpus import stopwords
import pandas as pd
import string
import re
from itertools import chain

briefings = glob.glob("../../data/interim/*.txt")

dates = []
remarks = []
for briefing in briefings:
    date = pd.to_datetime(briefing.split('_')[-1].split('.')[0], infer_datetime_format=True)
    with open(briefing,'r') as f:
        lines = f.readlines()
        for line in lines:
            # keep the longer remarks
            if len(line.split()) >= 16:
                remarks.append(line.rstrip().replace(r'’','\''))
                dates.append(date)

df = pd.DataFrame({'date':dates,'text':remarks})

df['normalized_text'] = df['text'].apply(lambda x: normalize(x))

# make bigrams

sentences = df['normalized_text'].values
sentence_stream = [sentence.split() for sentence in sentences] 
bigram = Phrases(sentence_stream, min_count=5, threshold=80)
trigram = Phrases(bigram[sentence_stream], threshold=80)
df['clean_text'] = df['normalized_text'].apply(lambda x: ' '.join(bigram[x.split()]))
df['clean_text'] = df['clean_text'].apply(lambda x: ' '.join(trigram[bigram[x.split()]]))

df.to_csv('trump_wh_remarks.csv')
