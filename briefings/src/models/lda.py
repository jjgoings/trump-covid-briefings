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

# pandas printing
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', None) 

sns.set_color_codes()

df = pd.read_csv('../../data/processed/trump_wh_remarks.csv')
remarks = [i.split() for i in list(df['clean_text'].values)]

common_dictionary = Dictionary(remarks)
common_dictionary.filter_extremes(no_below=10,no_above=0.0125, keep_tokens=['covid','coronavirus'])
print(common_dictionary)
common_corpus = [common_dictionary.doc2bow(remark) for remark in remarks]

num_topics=10
lda = LdaMulticore(common_corpus, id2word=common_dictionary,alpha='symmetric',num_topics=num_topics, workers=4,random_state=10) 

for topic in lda.print_topics():
    print(topic)

def format_topics_sentences(ldamodel=None, corpus=common_corpus, texts=remarks):
    # Init output
    sent_topics_df = pd.DataFrame()

    # Get main topic in each document
    for i, row_list in enumerate(ldamodel[corpus]):
        row = row_list[0] if ldamodel.per_word_topics else row_list            
        # print(row)
        row = sorted(row, key=lambda x: (x[1]), reverse=True)
        # Get the Dominant topic, Perc Contribution and Keywords for each document
        for j, (topic_num, prop_topic) in enumerate(row):
            if j == 0:  # => dominant topic
                wp = ldamodel.show_topic(topic_num)
                topic_keywords = ", ".join([word for word, prop in wp])
                sent_topics_df = sent_topics_df.append(pd.Series([int(topic_num), round(prop_topic,4), topic_keywords]), ignore_index=True)
            else:
                break
    sent_topics_df.columns = ['Dominant_Topic', 'Perc_Contribution', 'Topic_Keywords']

    # Add original text to the end of the output
    contents = pd.Series(texts)
    sent_topics_df = pd.concat([sent_topics_df, contents], axis=1)
    return(sent_topics_df)


df_topic_sents_keywords = format_topics_sentences(ldamodel=lda, corpus=common_corpus, texts=df['text'])

# Format
df_dominant_topic = df_topic_sents_keywords.reset_index()
df_dominant_topic.columns = ['Document_No', 'Dominant_Topic', 'Topic_Perc_Contrib', 'Keywords', 'Text']
#print(df_dominant_topic.head(10))

sent_topics_sorteddf_mallet = pd.DataFrame()
sent_topics_outdf_grpd = df_topic_sents_keywords.groupby('Dominant_Topic')

for i, grp in sent_topics_outdf_grpd:
    sent_topics_sorteddf_mallet = pd.concat([sent_topics_sorteddf_mallet, 
                                             grp.sort_values(['Perc_Contribution'], ascending=False).head(1)], 
                                            axis=0)

# Reset Index    
sent_topics_sorteddf_mallet.reset_index(drop=True, inplace=True)

# Format
sent_topics_sorteddf_mallet.columns = ['Topic_Num', "Topic_Perc_Contrib", "Keywords", "Representative Text"]

# Show
print(sent_topics_sorteddf_mallet.head(num_topics))

data_lda = {i: OrderedDict(lda.show_topic(i,12)) for i in range(num_topics)}
df_lda = pd.DataFrame(data_lda)
df_lda = df_lda.fillna(0).T
print(df_lda.shape)

g=sns.clustermap(df_lda.corr(), center=0, standard_scale=1, cmap="RdBu", metric='cosine', linewidths=.75, figsize=(8, 8))
plt.setp(g.ax_heatmap.yaxis.get_majorticklabels(), rotation=0)
#plt.show()

panel = pyLDAvis.gensim.prepare(lda, common_corpus, common_dictionary, mds='pcoa',R=20)
pyLDAvis.show(panel)
'''

#for above in np.arange(0.01,0.111,0.025):
#    for below in [0,5,10,15,20]:
#above = 0.025
below = 10
#common_dictionary = Dictionary(remarks)
#common_dictionary.filter_extremes(no_below=below,no_above=above)#, keep_tokens=['injury','science','data','choice'])
#print('# above: %s, # below: %s' % (above,below)) 
#print(common_dictionary)
#common_corpus = [common_dictionary.doc2bow(remark) for remark in remarks]

best_cv = 0.0
CVs = []
topics = []
for above in [0.01,0.02]:#,0.03]:
    CVs = []
    topics = []
    for num_topics in range(25,151,25):
        for alpha in ['symmetric']:#,'asymmetric']:
            common_dictionary = Dictionary(remarks)
            common_dictionary.filter_extremes(no_below=below,no_above=above)#, keep_tokens=['injury','science','data','choice'])
            #print('# above: %s, # below: %s' % (above,below)) 
            #print(common_dictionary)
            common_corpus = [common_dictionary.doc2bow(remark) for remark in remarks]
            lda = LdaMulticore(common_corpus, id2word=common_dictionary,num_topics=num_topics, alpha=alpha,workers=4,random_state=0) 
            # Compute Coherence Score
            coherence_model_lda = CoherenceModel(model=lda, corpus=common_corpus, texts=remarks,coherence='c_v')
            coherence_lda = coherence_model_lda.get_coherence()
            print('Topics: %s; alpha: %s; Coherence Score: %.4f' % (int(num_topics),alpha, coherence_lda))
            CVs.append(coherence_lda)
            topics.append(num_topics)
           
            if coherence_lda > best_cv:
                best_combo = 'BEST -- Topics: %s; alpha: %s; Coherence Score: %.4f' % (int(num_topics),alpha, coherence_lda)
                best_cv = coherence_lda
                
    print(best_combo,'\n')

    plt.plot(topics,CVs,label=above)
plt.legend()
plt.show()
'''
