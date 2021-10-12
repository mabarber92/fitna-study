# -*- coding: utf-8 -*-
"""
Created on Wed Jun 16 13:19:53 2021

@author: mathe
"""

import re
from collections import Counter
import pandas as pd

path = "C:/Users/mathe/Documents/Kitab project/Big corpus datasets/date_tagged_corpus/whole text tagger/outputs/0845Maqrizi.Mawaciz.Shamela0011566-ara1.date_tagged"

with open(path, encoding = "utf-8") as f:
    text = f.read()
    f.close()

years = re.findall(r"@YY\d{3}", text)

distinct = Counter(years)

distinct = dict(sorted(distinct.items(), key=lambda item: item[1]))    

# Get record of centuries

century_counts = []

for i in range(0,10):
    regex = r"@YY" + str(i) + "\d{2}"
    date_list = re.findall(regex, text)
    distinct_dates = Counter(date_list)    
    distinct_dates = dict(sorted(distinct_dates.items(), key=lambda item: item[1]))    
    df = pd.DataFrame.from_dict(distinct_dates, orient='index', columns = ["Distinct count"])
    df.to_csv("century_" + str(i) + ".csv")
    
    century_counts.append([str(i) + "00", len(distinct_dates), len(date_list)])

df_all = pd.DataFrame.from_dict(distinct, orient='index', columns = ["Distinct count"])
df_cen = pd.DataFrame(century_counts, columns = ["Date", "Distinct count", "Absolute count"])

df_all.to_csv("all_dates_distinct.csv")
df_cen.to_csv("centuries_distinct.csv")    

    




