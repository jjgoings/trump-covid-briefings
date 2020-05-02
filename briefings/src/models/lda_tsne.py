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
import matplotlib.colors as mcolors
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.neighbors import KDTree
from sklearn.manifold import TSNE
from nltk.cluster import KMeansClusterer
from gensim.models import word2vec, LdaMulticore
import nltk
from sklearn import cluster
from sklearn import metrics
from bokeh.plotting import figure, output_file, show, ColumnDataSource

# pandas printing
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', None) 

sns.set_color_codes()

df = pd.read_csv('../../data/processed/trump_wh_remarks.csv')
remarks = [i.split() for i in list(df['clean_text'].values)]

common_dictionary = Dictionary(remarks)
common_dictionary.filter_extremes(no_below=10,no_above=0.01, keep_tokens=['covid','coronavirus'])
print(common_dictionary)
common_corpus = [common_dictionary.doc2bow(remark) for remark in remarks]

num_topics=8
lda = LdaMulticore(common_corpus, id2word=common_dictionary,alpha='symmetric',num_topics=num_topics, workers=4,random_state=10) 

# Get topic weights and dominant topics ------------
from sklearn.manifold import TSNE
from bokeh.plotting import figure, output_file, show
from bokeh.models import Label
from bokeh.io import output_notebook

# Get topic weights
topic_weights = []
for i, row_list in enumerate(lda[common_corpus]):
    topic_weights.append([w for i,w in row_list])

#print(topic_weights)

# Array of topic weights
skip = 1
np.random.seed(0)
arr = pd.DataFrame(topic_weights).fillna(0).values
sample_idx = np.random.choice(arr.shape[0], int(np.floor(len(arr)/skip)), replace=False)
arr = arr[sample_idx]
#
## Keep the well separated points (optional)
#arr = arr[np.amax(arr, axis=1) > 0.35]
#
## Dominant topic number in each doc
topic_num = np.argmax(arr, axis=1)

#print(arr)

# tSNE Dimension Reduction
tsne_model = TSNE(n_components=2, verbose=1, random_state=0, perplexity=300, init='pca')
tsne_lda = tsne_model.fit_transform(arr)

# Plot the Topic Clusters using Bokeh
#output_notebook()
TOOLTIPS = """
    <div style="width:300px;">
    @remark
    </div>
    """

clrs = sns.color_palette('husl', n_colors=num_topics).as_hex()
label_color = [clrs[l] for l in topic_num]
mycolors = np.array([color for name, color in mcolors.TABLEAU_COLORS.items()])
source = ColumnDataSource(data=dict(
    x=tsne_lda[:,0],
    y=tsne_lda[:,1],
    color=label_color,
    remark=df['text'].iloc[sample_idx],
))


plot = figure(title="t-SNE Clustering of {} LDA Topics".format(num_topics),
              plot_width=900, plot_height=700, tooltips=TOOLTIPS)
plot.circle(x='x', y='y', color='color',source=source,size=8,fill_alpha=0.9,line_color='black')
show(plot)
