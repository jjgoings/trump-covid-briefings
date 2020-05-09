import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import NMF

sns.set_color_codes()

# I found that 6 topics makes the most sense
num_topics = 6

# Load data and make each document a day's briefing 
df = pd.read_csv('../../../data/processed/trump_wh_remarks.csv')
#print(df)
remarks = [i for i in list(df['clean_text'].values)]
full_remarks = [i for i in list(df['text'].values)]

# From sklearn example
def print_top_words(model, feature_names, n_top_words):
    for topic_idx, topic in enumerate(model.components_):
        message = "Topic #%d: " % topic_idx
        message += " ".join([feature_names[i]
                             for i in topic.argsort()[:-n_top_words - 1:-1]])
        print(message)
    print()

# Use tf-idf features for NMF.
print("Extracting tf-idf features for NMF...")

# Trump has a simple vocabulary, so we have to use more agressive cutoffs to isolate unique words
tfidf_vectorizer = TfidfVectorizer(max_df=0.01, min_df=5)
tfidf = tfidf_vectorizer.fit_transform(remarks)

print("NMF topics")
nmf = NMF(n_components=num_topics, random_state=1,
          alpha=.1, l1_ratio=.5).fit(tfidf)
tfidf_feature_names = tfidf_vectorizer.get_feature_names()
print_top_words(nmf, tfidf_feature_names, 10)

# adapted from https://towardsdatascience.com/improving-the-interpretation-of-topic-models-87fd2ee3847d
def display_topics(H, W, feature_names, remarks, no_top_words, no_top_remarks):
    for topic_idx, topic in enumerate(H):
        print("Topic %d:" % (topic_idx))
        print(" ".join([feature_names[i]
                        for i in topic.argsort()[:-no_top_words - 1:-1]]))
        top_doc_indices = np.argsort( W[:,topic_idx] )[::-1][0:no_top_remarks]
        for doc_index in top_doc_indices:
            print(remarks[doc_index])

nmf_W = nmf.transform(tfidf)
nmf_H = nmf.components_

print(nmf_W.shape)
#print(nmf_H.shape)
#print(tfidf.shape)

# Get percent topics
# NMF is non-probabilistic, but it will still "assign" documents
topics = []
for i in range(nmf_W.shape[0]):
    doc = nmf_W[i,:]
    if np.linalg.norm(doc) > 1e-6:
    #    print(nmf_W[i,:])
        topics.append(np.argmax(nmf_W[i,:]))

for i in range(num_topics):
    print(i+1, topics.count(i)/len(topics)*100, topics.count(i)/nmf_W.shape[0]*100)


#no_top_words = 10
#no_top_remarks = 10
#display_topics(nmf_H, nmf_W, tfidf_feature_names, full_remarks, no_top_words, no_top_remarks)

