# What does Trump talk about when he talks about COVID-19? 

<p align="center">
<img alt="" src="/assets/trump_wh_press_briefing.jpg" height="200" />
<img alt="" src="/assets/covid.png" height="200" />
</p>


<!---  * [What does Trump talk about?](#what-does-trump-talk-about) -->
## Table of Contents
* [Background](#background)
* [Findings](#findings)
  * [Keywords for each day's briefing](#keywords-for-each-days-briefing)
  * [How positive/negative is Trump during his speeches?](#how-positivenegative-is-trump-during-his-speeches)
  * [What might be influencing Trump's attitude?](#what-might-be-influencing-trumps-attitude)
* [Details on Data Acquisition](#details-on-data-acquisition)
<!---* [Usage](#usage)-->

## Background

Since March 14, 2020, President Trump has given semi-regular press updates on the global COVID-19 outbreak. While this pandemic is impacting nearly every aspect of everyday life, it is important to understand how our leaders perceive and communicate the next steps as we tackle these unprecedented issues. 

The New York Times (NYT) recently ran a [fascinating article](https://www.nytimes.com/interactive/2020/04/26/us/politics/trump-coronavirus-briefings-analyzed.html) that painstakingly analyzed over 260,000 words Trump has publicly spoken about the novel coronavirus. It took three journalists at the NYT to review all these statements *by hand*, and they found that the President's comments were particularly self-congratulatory, exaggerated, and startlingly lacking in empathy when compared to how often he praises himself and his administration. 

I wondered, though, if a more **data-driven** approach to Trump's remarks would yield any new insights. In particular, using data and natural language processing (NLP) to understand:

* What topics Trump thinks are particularly important?

* What are some of the keywords for each day's briefing? 

* Trump's attitude (sentiment) during his speeches?

* What underlying factors in the news or world correlate with his message?

Given that all his remarks are publicly recorded on the [White House webpage](https://www.whitehouse.gov/remarks/), I knew we had what we needed to answer these questions. 

## Findings

<!---### What does Trump talk about? -->

### Keywords for each day's briefing

It's interesting to see what Trump thinks is important each day. One way to address this is to pull out the top keywords for each day's briefing. The technique we use is term-frequency inverse-document-frequency (TF-IDF) and treat each day's briefing as a "document". It's a cheap and effective way to pull out those unique keywords that distinguish each day's briefing.

Here's an example of the important keywords found on March 14:

|    Date    |          Keyword 1         |      Keyword 2     |        Keyword 3        |        Keyword 4       |         Keyword 5        |
|:----------:|:--------------------------:|:------------------:|:-----------------------:|:----------------------:|:------------------------:|
| March 14 |                        fed |          proactive |                     mic |                closure |                refinance |

So here you can see that "mic" (or "microphone") was a keyword of interest. Interestingly, Trump went on a bit of a rant during his talk because he was accused of touching the microphone:

> Somebody said yesterday I touched the microphone.  I was touching it because we have different height people and I'm trying to make it easy for them because they're going to have to touch, because they wouldn't be able to reach the mic; they wouldn't be able to speak in the mic.  So I'll move the mic down.  And they said, "Oh, he touched the microphone."  Well, if I don't touch it, they’re going to have to touch it.  Somebody is going to have to, so I might as well be the one to do it. 

Amusing that the model identified this (somewhat) bizarre tangent.

You can see for yourself below. (Click to expand the table.) Near the beginning of the briefings, things seem much more focused on health-care and government action ("proactive", "self swab", "buyback"). But as the economy progressively gets worse (see March 23!) then we see more of an economic focus ("exchange", "cure is worse than the problem"). The economic shutdown is no small deal!

<details><summary><b> Click to show important keywords by day </b> </summary>

|    Date    |          Keyword 1         |      Keyword 2     |        Keyword 3        |        Keyword 4       |         Keyword 5        |
|:----------:|:--------------------------:|:------------------:|:-----------------------:|:----------------------:|:------------------------:|
| March 14 |                        fed |          proactive |                     mic |                closure |                refinance |
| March 15 |                    predict |    Federal Reserve |                  Google |                  relax |                    store |
| March 16 |                 postponing |            symptom |            Friday night |                   wash |                 Rochelle |
| March 17 |                payroll tax |             Boeing |              telehealth |                tourism |                 screened |
| March 18 |                  self swab |               calm |              invincible |                 target |                passenger |
| March 19 |                      Syria |        chloroquine |                    Tice |                 mother |                    chaos |
| March 21 |               student loan |            penalty |            inaccurately |                buyback |         religious leader |
| March 22 |                    veteran |                 VA | Federal Medical Station |            preexisting |                     rich |
| March 23 |                     Boeing | cure is worse than the problem |        watching closely |               exchange |                 learning |
| March 24 |                   timeline |       independence |                   Larry |          large section |              established |
| March 25 |                      Steve |           Olympics |             South Korea |          specification |             significance |
| March 26 |                      steel |              Brady |                     Tom |            South Korea |               96 |
| March 27 |               appreciative |              Peter |                smartest |                 Boeing |                   handle |
| March 30 |                   June 1st |             rating |                   waive | 300,000 |        22 million |
| March 31 |                      scarf |              guest |                    ride |              impeached |                      oil |
| April 01 |                       cash |           violence |                   train |                  Logan |                 Facebook |
| April 02 |                    gesture |                cut |                    flat |                   Iran |                     bump |
| April 03 |                   voter id |         81 |               voluntary |                   mail |                      oil |
| April 04 |              whistleblower |         transcript |                informer |           commissioner |   180 |
| April 05 | 182 |                sue |                 rushing |                    oil |                     sign |
| April 06 |                     letter |             London |               intensive |                nuclear |              replacement |
| April 08 |                   delegate |             Bernie |                    memo |                 Easter |                   voting |
| April 09 |                        oil |             mental |                  Scalia |                storage |                     OPEC |
| April 10 |                     pastor |             Denver |            interruption |                 Mexico | World Trade Organization |
| April 13 |                    January |          committee |                    clip |           Jan 17th |                    Wuhan |
| April 15 |                      judge |           approved |                   Sonny |                session |                  nominee |
| April 16 |                      count |               wide |                   arena |             devastated |                 capacity |
| April 19 |                       swab |            aroused |                     ran |               pressure |                    hotel |
| April 20 |                  defending |            squeeze |             sustainable |         60,000 |                    rally |
| April 22 |                     corona |             parlor |               misquoted |                  ember |                      flu |
| April 23 |                        sun |               heat |              laboratory |                surface |               Brian Kemp |
| April 24 |                    Stephen |          approving |                declined |                payment |                      Tim |
| April 27 |                   pharmacy |             damage |        Attorney General |          General Flynn |                  quarter |

</details>

You can also see the importance of oil in April. It wasn't a huge issue, but you see it become more important starting around April 3, peaking around April 9. That day, if you recall, was when OPEC made *huge* cuts in oil production. So naturally it was a topic in Trump's briefing that day! 

### How positive/negative is Trump during his speeches?

We can investigate how positive or negative Trump is speaking during his briefings. To do this, we look at the compound sentiment for each briefing using the Valence Aware Dictionary and sEntiment Reasoner ([VADER](http://comp.social.gatech.edu/papers/icwsm14.vader.hutto.pdf)). Although it was trained on social media, it works well for our purposes. It ranges from -1 (negative) to +1 (positive). You can see that, on the whole, Trump is pretty positive-to-neutral. Politically, I think this would be better to lean positive during the briefings. Of course, you don't want to be too positive either during these tough times!

<p align="center">
<img alt="" src="/briefings/src/models/vader/sentiment.png" width="800" />
</p>

On average, his sentiment lies around 0.4, with a standard deviation of 0.1. So leaning positive, but by no means elated, which is probably the right tone to hit.  

### What might be influencing Trump's attitude?

Perhaps more interesting is to try and find patterns in Trump's sentiment. Initially, I noticed the big spike in sentiment on March 24, as well as a pretty big drop in sentiment on April 1. On March 24, there was a big stock market rally, and on April 1, the market suffered a few days of losses. I wondered: could it be that Trump's mood is correlated with stock market performance? 

To investigate, I plotted Trump's sentiment versus the percent change in the closing value of the Dow Jones Industrial Average. On first look, you can see that the briefing sentiment shows some correlation with changes in thew DJIA. If the market is doing bad, Trump is generally more negative, and if the market is doing well, Trump is more positive. It's tough to say which direction the correlation goes (correlation is not causation!) but given that Trump usually holds his briefings later in the day, I'm inclined to think the market bears more influence on his mood. But the issues are complicated and there are many more variables at play, so take it with a grain of salt. 

<p align="center">
<img alt="" src="/briefings/src/models/vader/sentiment_vs_djia.png" width="800" />
</p>

We can actually make the correlation between stock market and Trump's mood a bit tighter. Below we have a regression plot, and find that the Pearson correlation is around +0.45. This is good enough to say that there is likely a moderate positive correlation between Trump's sentiment and the market performance. Makes sense, as he prides himself on his business acumen and being able to keep the American economy strong. (No comment if that corresponds to reality.)

<p align="center">
<img alt="" src="/briefings/src/models/vader/sentiment_vs_djia_correlation.png" width="800" />
</p>

## Details on Data Acquisition

The raw data was scraped from [https://www.whitehouse.gov/remarks/](https://www.whitehouse.gov/remarks/) using `requests` and `BeautifulSoup4`. For now, all we explore Trump's statements during the Coronavirus Task Force press meetings (which as of today, May 6, may be ending). 

The president's name is listed before he speaks, so once the page is downloaded locally, it is relatively easy to extract just Trump's statements. We treat a "statement" as any of Trump's spoken words separated by a newline. This gave a variety of statements, usually around 3 to 5 sentences long. If any statement was less than 16 words, we ignored it (these usually are statements like "Thank you John, next question", etc.) as these are not meaningful. If a statement was too long (longer than 140 words) we split them into smaller chunks. This foresight allows us to use the BERT transformer in future work, which in the default model cannot handle sentences with more than 512 word embeddings.

Once the raw text was extracted to a `pandas` DataFrame, we applied standard text-cleaning routines to make all lowercase, remove stopwords, and add bigrams and trigrams (so '`mayor`', '`de`', '`blasio`' is not three separate words, but instead is treated as '`mayor_de_blasio`', which is much more informative!).

After cleaning, the data is saved in `briefings/data/processed/trump_wh_remarks.csv` for further NLP analysis.

<!---## Usage-->

