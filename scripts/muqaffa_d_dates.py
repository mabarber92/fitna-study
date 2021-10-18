# -*- coding: utf-8 -*-
"""
Created on Thu Oct 14 16:54:43 2021

@author: mathe
"""

import re
import pandas as pd
import os
from tqdm import tqdm


def count_dates_muq(text, on = "head", tops = False, w_counts = False):
    if on == "head":
        split_seps = re.split(r"(###\s\|\|\|\s)", text)
        splits = []
        for split_sep in split_seps:
            if split_sep != "### ||| ":
                splits.append("### ||| " + split_sep)
    if on == "ms":
        splits = re.split(r"ms\d+", text)
    
    out = []
    columns = ["section"]
    if w_counts:
        columns.append("st_pos")
        columns.append("mid_pos")
        columns.append("w_count")
    
    
    columns.append("date")
    columns.append("century")
    columns.append("25-y")
    columns.append("Name")
    
    if tops:
        columns.append("Topic_id")
    
    word_counter = 0
 
    
    
    for idx, split in enumerate(tqdm(splits)):
        
        temp = [idx + 1]
        
        if w_counts:
            temp.append(word_counter)
            sec_length = len(re.split(r"\s", split))
            temp.append(word_counter + (sec_length/2))
            word_counter = word_counter + sec_length
            temp.append(sec_length)
            
            
        d_dates = re.findall("###\s\|\|\|.*-\s.*\[-?\D*(\d{1,3})\]", split)
        
        if len(d_dates) >= 1:
            d_date = d_dates[0]
            
            if len(d_date) == 2:
                d_date = "0" + d_date
            elif len(d_date) == 1:
                d_date = "00" + d_date
            
            century = int(d_date[0] + "00")
            if int(d_date[1:3]) <= 25:
                y25 = century + 25
                
            elif int(d_date[1:3]) <= 50:
                y25 = century + 50
                
            elif int(d_date[1:3]) <= 75:
                y25 = century + 75
                
            else:
                if century == 0:
                    y25 = 100
                else:
                    y25 = century + 100
                
            
            name = re.findall("###\s\|\|\|.*-\s(.*)\[.*\]?", split)[0]
            
            temp.extend([int(d_date), century, str(y25), name])
        else:
            continue
        
            
        if tops:            
            topic = re.findall(r"@TPC@(\d+)@", split)
            if len(topic) >= 1:
                temp.append(int(topic[0]))
            else:
                temp.append(0)
        
        out.append(temp)
    
    out_df = pd.DataFrame(out, columns = columns)
    
    return out_df

path_parent = os.path.dirname(os.getcwd())

path = path_parent + "/whole text tagger/inputs/0845Maqrizi.Muqaffa.Shamela19Y0145334-ara1"

with open(path, encoding = "utf-8") as f:
    text = f.read()
    f.close()


out = count_dates_muq(text, w_counts = True)

out.to_csv("muq_bio_dates.csv", index = False)