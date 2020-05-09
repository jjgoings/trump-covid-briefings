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
remarks = [i for i in list(df['clean_text'].values)]

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


