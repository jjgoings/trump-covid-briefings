import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from nltk.cluster import KMeansClusterer
from gensim.models import word2vec, LdaMulticore, ldaseqmodel, CoherenceModel
from gensim.corpora.dictionary import Dictionary
from gensim.test.utils import common_texts
import pyLDAvis
import pyLDAvis.gensim
from collections import OrderedDict

df = pd.read_csv('../../data/processed/trump_wh_remarks.csv')
remarks = [i.split() for i in list(df['clean_text'].values)]

best_cv = 0.0
CVs = []
topics = []
for num_topics in range(2,21,1):
    common_dictionary = Dictionary(remarks)
    common_dictionary.filter_extremes(no_below=10,no_above=0.0125, keep_tokens=['covid','coronavirus'])
    common_corpus = [common_dictionary.doc2bow(remark) for remark in remarks]
    lda = LdaMulticore(common_corpus, id2word=common_dictionary,num_topics=num_topics, alpha='symmetric', workers=4,random_state=10) 

    # Compute Coherence Score
    coherence_model_lda = CoherenceModel(model=lda, corpus=common_corpus, texts=remarks,coherence='c_v')
    coherence_lda = coherence_model_lda.get_coherence()
    print('Topics: %s; Coherence Score: %.4f' % (int(num_topics), coherence_lda))
    topics.append(num_topics)
    CVs.append(coherence_lda)
   
    if coherence_lda > best_cv:
        best_combo = 'BEST -- Topics: %s; Coherence Score: %.4f' % (int(num_topics), coherence_lda)
        best_cv = coherence_lda
        
print(best_combo,'\n')
plt.plot(topics,CVs)
plt.xlabel('# Topics')
plt.ylabel('Coherence')
plt.legend()
plt.show()
