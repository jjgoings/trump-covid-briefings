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

stocks = stocks.reindex(pd.date_range("2020-03-13", "2020-04-27"), method='ffill')
stocks['pct_chg'] = stocks['Adj Close'].pct_change()
#print(stocks)

data['sentiment'] = sentiment
data = data.groupby(['date']).mean()
data.index = pd.to_datetime(data.index)
data = data.reindex(pd.date_range("2020-03-13", "2020-04-27"), fill_value=0.0)
#print(data)

#plot data
fig, (ax,ax2) = plt.subplots(2, figsize=(10,8), sharex=True, gridspec_kw={'hspace': 0})

ax.bar(data.index, data['sentiment'],color='gray')

#set ticks every week on Monday
ax2.xaxis.set_major_locator(mdates.WeekdayLocator(byweekday=MO))
ax2.xaxis.set_minor_locator(mdates.DayLocator())

#set major ticks format
ax2.xaxis.set_major_formatter(mdates.DateFormatter('%b %d'))
#ax2.plot(stocks.index,stocks['Adj Close'])
ax2.plot(stocks.index,stocks['pct_chg'],lw=2,color='black')
ax.set_ylim([0.15,0.75])
ax2.set_ylim([-0.14,0.14])
ax2.set_yticks(np.arange(-0.1, 0.11, 0.1))
ax.xaxis.grid(True,zorder=-100)
ax2.xaxis.grid(True,zorder=-100)
ax.set_ylabel("Trump's Attitude")
ax2.set_ylabel('% Change in Dow Jones')
ax2.fill_between(stocks.index, 0, stocks['pct_chg'], where=stocks['pct_chg'] >= 0, facecolor='green', alpha=0.6,interpolate=True)
ax2.fill_between(stocks.index, 0, stocks['pct_chg'], where=stocks['pct_chg'] <= 0, facecolor='red', alpha=0.6, interpolate=True)
ax.get_yaxis().set_label_coords(-0.075,0.5)
ax2.get_yaxis().set_label_coords(-0.075,0.5)
plt.xlabel('Date')
plt.savefig('sentiment_vs_djia.png',dpi=300,bbox_inches='tight')
plt.show()
plt.close()




