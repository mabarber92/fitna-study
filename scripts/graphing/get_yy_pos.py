# -*- coding: utf-8 -*-
"""
Created on Mon Aug  8 12:27:29 2022

@author: mathe
"""

import re
import pandas as pd
from tqdm import tqdm
import os

def get_yy_pos(text_path, out_path, colour_map = None):
    """Colour map to follow dict format of {'beg': 1, 'end': 100, 'label': 'first-century', 'colour': 'purple'}"""
    
    with open(text_path, encoding = "utf-8") as f:
        text = f.read()
        f.close()
    
    # Remove section markers - as these are removed when counting chars for sections
    text = re.sub(r"###\s", "", text)
    
    matches = re.finditer(r"@YY(\d+)", text)
    
    out = []
    
    for match in tqdm(matches):
        row = {}
        date = int(match.group(1))
        row["pos"] = match.start()
        row["date"] = date
        if colour_map is not None:
            for mapping in colour_map:
                if date >= mapping["beg"] and date < mapping["end"]:
                    row["label"] = mapping["label"]
                    row["colour"] = mapping["colour"]
        out.append(row)
    
    out_df = pd.DataFrame(out)
    out_df.to_csv(out_path)


in_path = "C:/Users/mathe/Documents/Github-repos/fitna-study/whole text tagger/outputs/dates_tagged_new"
out_path = "C:/Users/mathe/Documents/Github-repos/fitna-study/dates_analysis/mappings_updated_chars/"


cats = [{'beg': 1, 'end': 100, 'label': 'first-century', "colour" : "saddlebrown"}, 
        {'beg': 101, 'end': 357, 'label': 'pre-fatimid', "colour" : "orange"}, 
        {'beg': 358, 'end': 567, 'label': 'fatimid', "colour": "green"},
        {'beg': 568, 'end': 648, 'label': 'ayyubid', "colour": "red"},
        {'beg': 649, 'end': 900, 'label': 'mamluk', "colour": "blue"}]


for root, dirs, files in os.walk(in_path, topdown=False):
    for name in tqdm(files):
        print(name)            
        text_path = os.path.abspath(os.path.join(root, name))
        full_out_path = out_path + name + ".yy_mapped.csv"
        
        get_yy_pos(text_path, full_out_path, colour_map = cats)