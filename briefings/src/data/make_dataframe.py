import glob
from clean_text import preprocess
import pandas as pd
import re

briefings = glob.glob("../../data/interim/*.txt")

dates = []
remarks = []
for briefing in briefings:
    date = pd.to_datetime(briefing.split('_')[-1].split('.')[0], infer_datetime_format=True)
    with open(briefing,'r') as f:
        lines = f.readlines()
        for line in lines:
            # keep the longer remarks
            if len(line.split()) >= 16:
                remarks.append(line.rstrip().replace(r'’','\''))
                dates.append(date)

df = pd.DataFrame({'date':dates,'text':remarks})

df['clean_text'] = df['text'].apply(lambda x: preprocess(x))

df.to_csv('trump_wh_remarks.csv')
    

