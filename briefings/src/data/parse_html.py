from bs4 import BeautifulSoup
from datetime import date
import unicodedata
import glob
import re

def clean_html(text):
    # remove HTML tags, normalize unicode, and strip newlines/whitespace at ends
    return unicodedata.normalize('NFKD',re.sub('<[^<]+?>', '', str(text))).strip()

briefings = glob.glob("../../data/raw/*.html")

for briefing in briefings:
    page = open(briefing)
    soup = BeautifulSoup(page.read(),features="lxml")
    text = soup.find_all('p')
    isTrump = False
    lines = []
    for line in text:
        # We don't want any newlines
        cleaned_line = clean_html(line).replace('\n', ' ')
        cleaned_line = cleaned_line.replace('•', '\n')
        if cleaned_line[:5].isupper(): # actors are in all upper case for at least 5 characters long
            if cleaned_line[:14] == 'THE PRESIDENT:':
                isTrump = True 
            else:
                isTrump = False
        if isTrump:
            # print Trump's remarks, cutting out the actor's name
            if cleaned_line[:14] == 'THE PRESIDENT:':
                lines.append(re.sub(' +', ' ',cleaned_line[14:]).strip())
            # don't print things like "(Cross talk.)"
            elif (cleaned_line[0] == '(') and (cleaned_line[-1] == ')'):
                continue
            else:
                lines.append(re.sub(' +', ' ',cleaned_line).strip())

    date = briefing.split('_')[-1].split('.')[0]
    filename = 'trump_raw_text_'+date+'.txt'
    with open(filename,'w') as f:
        for line in lines:
            print(line,file=f)
    

