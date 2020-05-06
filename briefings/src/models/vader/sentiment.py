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
data.index = pd.to_datetime(data.index)
#data = data.reindex(pd.date_range("2020-03-13", "2020-04-30"), fill_value=0.0)

#plot data
fig, ax = plt.subplots(figsize=(10,6))

ax.bar(data.index, data['sentiment'],color='g')

#set ticks every week on Monday
ax.xaxis.set_major_locator(mdates.WeekdayLocator(byweekday=MO))
ax.xaxis.set_minor_locator(mdates.DayLocator())

#set major ticks format
ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %d'))

plt.ylim([0.15,0.65])
plt.ylabel('Sentiment')
plt.xlabel('Date')
plt.show()

