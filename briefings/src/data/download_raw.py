from bs4 import BeautifulSoup
from datetime import date
import requests
import unicodedata
import re

base_url = "https://www.whitehouse.gov/briefings-statements/remarks-president-trump-vice-president-pence-members-coronavirus-task-force-press-briefing"

def clean_html(text):
    # remove HTML tags, normalize unicode, and strip newlines/whitespace at ends
    return unicodedata.normalize('NFKD',re.sub('<[^<]+?>', '', str(text))).strip()

for page in range(1,34): # there are 33, as of today (04/29/2020)
    if page > 1:
        briefing_url = base_url + "-" + str(page)
    else:
        # first briefing has no enumeration
        briefing_url = base_url

    data = requests.get(briefing_url).text

    page = BeautifulSoup(data,features="lxml")
    # date issued usually works, but sometimes is not date briefing was held!
    date = [x for x in re.split(r'\,|\s',page.find('time').text) if x]
    month = date[0]
    day = date[1]
    year = date[2]

    # see if date issued is same as date on webpage text 
    text = page.find_all('p')
    alt_month = None
    for idx, line in enumerate(text):
        date_line = clean_html(line).split('\n')
        if (len(date_line) > 1) and ("2020" in date_line[0]) and ("EDT" in date_line[1]):
            alt_date = re.split(r'\,|\s',date_line[0]) 
            alt_month = alt_date[0]
            alt_day = alt_date[1]
            alt_year = alt_date[3]

    # sometimes it's in a <div> element ... sigh
    if not alt_month:
        text = page.find_all('div')
        for idx, line in enumerate(text):
            date_line = clean_html(line).split()
            if (len(date_line) == 3) and ("2020" in date_line):
                alt_date = date_line 
                alt_month = alt_date[0]
                alt_day = alt_date[1].replace(r',','')
                alt_year = alt_date[2]

    # now make some changes if an alternate date was found 
    if alt_month:
        if (alt_month,alt_day,alt_year) == (month, day, year):
            continue 
        else:
            month = alt_month
            day = alt_day
            year = alt_year
    
    
    webpage = 'white_house_briefing_%s-%s-%s.html' % (month, str(day).zfill(2), year)
    with open(webpage,'w') as f:
        f.write(page.prettify())
    


