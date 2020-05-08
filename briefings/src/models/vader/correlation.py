import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.dates import MO, TU, WE, TH, FR, SA, SU
import matplotlib as mpl
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import yfinance as yf

sns.set_color_codes()

np.random.seed(0)

data = pd.read_csv('../../../data/processed/trump_wh_remarks.csv')

analyzer = SentimentIntensityAnalyzer()
sentiment = []
for sentence in data['text']:
    vs = analyzer.polarity_scores(sentence)
    sentiment.append(vs['compound'])
    #print("{:-<65} {}".format(sentence, str(vs)))

stocks = yf.download('^DJI', 
             start='2020-03-13', 
             end='2020-04-27', 
             progress=False)

#stocks = stocks.reindex(pd.date_range("2020-03-13", "2020-04-27"), method='ffill')
stocks['pct_chg'] = stocks['Adj Close'].pct_change()

data['sentiment'] = sentiment
data = data.groupby(['date']).mean()
data.index = pd.to_datetime(data.index)
data.index.name = 'Date'
merge=pd.merge(data,stocks, how='inner', left_index=True, right_index=True)

fog,ax = plt.subplots()
R = np.corrcoef(merge['sentiment'].values.astype(float),merge['pct_chg'].astype(float))[1,0]
print(R)
print(R*R)
sns.regplot(x='sentiment',y='pct_chg',data=merge)
plt.xlabel("Trump's Attitude")
plt.ylabel('% Change in Dow Jones')

textstr = '{}{:.2f}'.format("Pearson Correlation: ",R) 

# these are matplotlib.patch.Patch properties
props = dict(facecolor='white', edgecolor='white',alpha=0.0)

# place a text box in upper left in axes coords
ax.text(0.5, 0.06, textstr, transform=ax.transAxes, fontsize=14,
        verticalalignment='top', bbox=props)

plt.savefig('sentiment_vs_djia_correlation.png',bbox_inches='tight',dpi=300)
plt.show()


