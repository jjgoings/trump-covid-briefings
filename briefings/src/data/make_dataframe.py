import glob
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
            remarks.append(line.rstrip().replace(r'’','\''))
            dates.append(date)

df = pd.DataFrame({'date':date,'text':remarks})

df.to_csv('trump_wh_remarks.csv')
    

