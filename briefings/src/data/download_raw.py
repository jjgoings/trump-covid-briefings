from bs4 import BeautifulSoup
from datetime import date
import requests
import re

base_url = "https://www.whitehouse.gov/briefings-statements/remarks-president-trump-vice-president-pence-members-coronavirus-task-force-press-briefing"

for page in range(34): # there are 34, as of today (04/29/2020)
    if page > 1:
        briefing_url = base_url + "-" + str(page)
    else:
        # first briefing has no enumeration
        briefing_url = base_url

    data = requests.get(briefing_url).text

    page = BeautifulSoup(data,features="lxml")
    date = [x for x in re.split(r'\,|\s',page.find('time').text) if x]
    month = date[0]
    day = date[1]
    year = date[2]
    
    webpage = 'white_house_briefing_%s-%s-%s.html' % (month, str(day).zfill(2), year)
    with open(webpage,'w') as f:
        f.write(page.prettify())
    


