from datetime import date
import glob
import re

briefings = glob.glob("../../data/interim/*.txt")[0:1]
print(briefings)

for briefing in briefings:
    date = briefing.split('_')[-1].split('.')[0]
    print(date)
    with open(briefing,'r') as f:
        lines = f.readlines()
        for line in lines:
            print(line.rstrip())

    

