# -*- coding: utf-8 -*-
"""
Created on Wed Aug 24 17:02:39 2022

@author: mathe
"""

import re

def measure_gap(text_path, year):
    with open(text_path, encoding = 'utf-8-sig') as f:
        text = f.read()
        f.close()
    regex= "@YY" + str(year)
    results = re.finditer(regex, text)
    gaps = []
    pos_store = 0
    for result in results:
        gaps.append(result.start() - pos_store)
        pos_store = result.start()
    
    average_gap = sum(gaps)/len(gaps)
    print(average_gap)
    return gaps, average_gap


text_path = "C:/Users/mathe/Documents/Github-repos/fitna-study/whole text tagger/outputs/dates_tagged_new/0845Maqrizi.Mawaciz.MAB02082022-ara1.completed.dates_tagged"
gaps, average_gap = measure_gap(text_path, 790)
        