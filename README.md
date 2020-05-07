# What does Trump talk about when he talks about COVID-19? 

## Table of Contents
* [Background](#background)
* [Findings](#findings)
  * [What does Trump talk about?](#what-does-trump-talk-about)
  * [How positive/negative is Trump during his speeches?](#how-positivenegative-is-trump-during-his-speeches)
  * [What might be influencing Trump's attitude?](#what-might-be-influencing-trumps-attitude)
* [Details on Data Acquisition](#details-on-data-acquisition)
* [Usage](#usage)

## Background

Since March 14, 2020, President Trump has given semi-regular press updates on the global COVID-19 outbreak. While this pandemic is impacting nearly every aspect of everyday life, it is important to understand how our leaders perceive and communicate the next steps as we tackle these unprecedented issues. 

The New York Times (NYT) recently ran a [fascinating article](https://www.nytimes.com/interactive/2020/04/26/us/politics/trump-coronavirus-briefings-analyzed.html) that painstakingly analyzed over 260,000 words Trump has publicly spoken about the novel coronavirus. It took three journalists at the NYT to review all these statements *by hand*, and they found that the President's comments were particularly self-congratulatory, exaggerated, and startlingly lacking in empathy when compared to how often he praises himself and his administration. 

I wondered, though, if a more **data-driven** approach to Trump's remarks would yield any new insights. In particular, using data and natural language processing (NLP) to understand:

* What topics Trump thinks are particularly important?

* Trump's attitude (sentiment) during his speeches?

* What underlying factors in the news or world correlate with his message?

Given that all his remarks are publicly recorded on the [White House webpage](https://www.whitehouse.gov/remarks/), I knew we had what we needed to answer these questions. 

## Findings

### What does Trump talk about?

### How positive/negative is Trump during his speeches?

### What might be influencing Trump's attitude?

<p align="center">
<img alt="" src="/briefings/src/models/vader/sentiment_vs_djia.png" width="800" />
</p>

## Details on Data Acquisition

The raw data was scraped from [https://www.whitehouse.gov/remarks/](https://www.whitehouse.gov/remarks/) using `requests` and `BeautifulSoup4`. For now, all we explore Trump's statements during the Coronavirus Task Force press meetings (which as of today, May 6, may be ending). 

The president's name is listed before he speaks, so once the page is downloaded locally, it is realtively easy to extract just Trump's statements. We treat a "statement" as any of Trump's spoken words separated by a newline. This gave a variety of statements, usually around 3 to 5 sentences long. If any statement was less than 16 words, we ignored it (these usually are statements like "Thank you John, next question", etc.) as these are not meaningful. If a statement was too long (longer than 140 words) we split them into smaller chunks. This foresight allows us to use the BERT transformer in future work, which in the default model cannot handle sentences with more than 512 word embeddings.

Once the raw text was extracted to a `pandas` DataFrame, we applied standard text-cleaning routines to make all lowercase, remove stopwords, and add bigrams and trigrams (so '`mayor`', '`de`', '`blasio`' is not three separate words, but instead is treated as '`mayor_de_blasio`', which is much more informative!).

After cleaning, the data is saved in `briefings/data/processed/trump_wh_remarks.csv` for further NLP analysis.

## Usage

