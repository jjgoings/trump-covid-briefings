import pandas as pd
from tqdm import tqdm
import numpy as np
import ast
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.neighbors import KDTree
from sklearn.manifold import TSNE
from sklearn.decomposition import PCA
from wordcloud import WordCloud
#from nltk.cluster import KMeansClusterer
#from gensim.models import word2vec
#import nltk
from sklearn import cluster
from sklearn import metrics
from bokeh.plotting import figure, output_file, show, ColumnDataSource
from bokeh.models.annotations import Legend
import tensorflow as tf
import umap
from collections import Counter 
from transformers import pipeline
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import yfinance as yf

sns.set_color_codes()

np.random.seed(0)

print("Loading remarks")
df = pd.read_csv('../../../data/processed/trump_wh_remarks.csv')

#X = np.load('bert-embeddings.npy')

analyzer = SentimentIntensityAnalyzer()
sentiment = []
for sentence in df['text']:
    vs = analyzer.polarity_scores(sentence)
    sentiment.append(vs['compound'])
    #print("{:-<65} {}".format(sentence, str(vs)))

stocks = yf.download('^DJI', 
             start='2020-03-13', 
             end='2020-04-30', 
             progress=False)

df['sentiment'] = sentiment
df2 = df.groupby(['date']).mean()
df2.index = pd.to_datetime(df2.index)
df2.index.name = 'Date'

print(stocks.index)
print(df2.index)

merge=pd.merge(df2,stocks, how='inner', left_index=True, right_index=True)
print(merge)

fig = plt.figure() # Create matplotlib figure

ax1 = fig.add_subplot(111) # Create matplotlib axes
ax2 = ax1.twinx() # Create another axes that shares the same x-axis as ax.

width = 0.4

merge['pct_chg'] = merge['Adj Close'].pct_change()
merge['diff'] = merge['Adj Close'].diff()

merge['Adj Close'].plot(kind='bar', color='r', ax=ax1, width=width, position=1)
merge['sentiment'].plot(kind='bar', color='b', ax=ax2, width=width, position=0)

#merge['Adj Close'].plot(kind='line', color='r', ax=ax1)#,  position=1)
#merge['sentiment'].plot(kind='line', color='b', ax=ax2)#,  position=0)
from matplotlib.lines import Line2D
custom_lines = [Line2D([0], [0], color='r', ls='-'),
                Line2D([0], [0], color='b', ls='-')]

ax1.legend(custom_lines, ['Adj Close','Sentiment'],loc='best')

ax1.set_ylabel('Adj Close',color='r')
ax1.set_ylim([19500,24500])
ax2.set_ylabel('Sentiment',color='b')

plt.show()

plt.close()

print(merge.corr())
sns.regplot(x="diff", y="sentiment", data=merge)
plt.xlabel('Daily Change in Dow Jones')
plt.ylabel('Average Briefing Sentiment')
plt.show()

