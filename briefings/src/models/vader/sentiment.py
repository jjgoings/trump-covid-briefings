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

data['sentiment'] = sentiment
data = data.groupby(['date']).mean()

avg_sentiment = data['sentiment'].mean()
std_sentiment = data['sentiment'].std()

print(avg_sentiment,std_sentiment)
data.index = pd.to_datetime(data.index)
#data = data.reindex(pd.date_range("2020-03-13", "2020-04-30"), fill_value=0.0)

#plot data
fig, ax = plt.subplots(figsize=(10,6))

ax.bar(data.index, data['sentiment'],color='gray')

#set ticks every week on Monday
ax.xaxis.set_major_locator(mdates.WeekdayLocator(byweekday=MO))
ax.xaxis.set_minor_locator(mdates.DayLocator())

#set major ticks format
ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %d'))
ax.xaxis.grid(True,zorder=-100)
date_range = pd.date_range("2020-03-11", "2020-04-30")
xmin = date_range[0]
xmax = date_range[-1]
plt.hlines(avg_sentiment,xmin,xmax,lw=2,ls='dashed')
plt.xlim([xmin,xmax])

textstr = '{}{:.2f}$\pm${:.2f}'.format("Average Sentiment: ",avg_sentiment,std_sentiment)

# these are matplotlib.patch.Patch properties
props = dict(facecolor='white', edgecolor='black',alpha=1.0)

# place a text box in upper left in axes coords
ax.text(0.05, 0.9, textstr, transform=ax.transAxes, fontsize=14,
        verticalalignment='top', bbox=props)

plt.ylim([0.15,0.75])
plt.ylabel("Trump's Attitude")
plt.xlabel('Date')
plt.savefig('sentiment.png',bbox_inches='tight',dpi=300)
#plt.show()

