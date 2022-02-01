# -*- coding: utf-8 -*-
"""
Created on Wed Jun 16 13:19:53 2021

@author: mathe
"""

import re
from collections import Counter
import pandas as pd
import os
from tqdm import tqdm


def count_y_centuries(text_path, out_path, centuries = True):

    with open(text_path, encoding = "utf-8") as f:
        text = f.read()
        f.close()

    years = re.findall(r"@YY(\d{3})", text)

    distinct = Counter(years)

    distinct = dict(sorted(distinct.items(), key=lambda item: item[1]))    

    # Get record of centuries if true
    
    if centuries:

        century_counts = []
        
        for i in range(0,10):
            regex = r"@YY(" + str(i) + "\d{2})"
            date_list = re.findall(regex, text)
            distinct_dates = Counter(date_list)    
            distinct_dates = dict(sorted(distinct_dates.items(), key=lambda item: item[1]))    
            df = pd.DataFrame.from_dict(distinct_dates, orient='index', columns = ["Distinct count"])
            df.to_csv("century_" + str(i) + ".csv")
            
            century_counts.append([str(i) + "00", len(distinct_dates), len(date_list)])
    
        df_cen = pd.DataFrame(century_counts, columns = ["Date", "Distinct count", "Absolute count"])
    
    df_all = pd.DataFrame.from_dict(distinct, orient='index', columns = ["Distinct count"])


    df_all.to_csv(out_path + ".all_dates_distinct.csv")
    df_cen.to_csv(out_path + ".centuries_distinct.csv")    


texts_input = "C:/Users/mathe/Documents/Github-repos/fitna-study/whole text tagger/outputs/for_update"
output_loc = "C:/Users/mathe/Documents/Github-repos/fitna-study/dates_analysis/date_freqs/"

for root, dirs, files in os.walk(texts_input, topdown=False):
    for name in tqdm(files):            
        text_path = os.path.abspath(os.path.join(root, name))    
        out_path = os.path.abspath(os.path.join(output_loc, name))
        count_y_centuries(text_path, out_path)



