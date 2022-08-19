# -*- coding: utf-8 -*-
"""
Created on Wed Jun 16 14:51:43 2021

@author: mathe
"""
import re
import pandas as pd
from pattern_mapping_cat import pattern_map_cat

def pattern_map(text, terms, on = "head", tops = False, w_counts = False):
    """!!CAUTION DEPRECATION THIS IS AN OLDER DEDICATED FUNCTION - TERMS COUNTING IS NOW BUNDLED INTO pattern_map_cat for broader functionality!!"""
    if on == "head":
        splits = re.split(r"###\s", text)
    if on == "ms":
        splits = re.split(r"ms\d+", text)
    
    terms_copy = terms[:]
    for term in terms:
        count = len(re.findall(term, text))
        if count == 0:
            terms_copy.remove(term)
    
    out = []
    columns = ["section"]
    if w_counts:
        columns.append("st_pos")
        columns.append("mid_pos")
    columns.extend(terms_copy)
    if tops:
        columns.append("Topic_id")
    
    word_counter = 0
 
 
    
    for idx, split in enumerate(splits):
        print('.', end = '')
        temp = [idx + 1]
        if w_counts:
            temp.append(word_counter)
            sec_length = len(re.split(r"\s", split))
            temp.append(word_counter + (sec_length/2))
            word_counter = word_counter + sec_length
            
            
            
                
        for term in terms_copy:            
            count = len(re.findall(term, split))
            temp.append(count)
        if tops:            
            topic = re.findall(r"@TPC@(\d+)@", split)
            if len(topic) >= 1:
                temp.append(int(topic[0]))
            else:
                temp.append(0)
        out.append(temp)
    
    out_df = pd.DataFrame(out, columns = columns)
    
    return out_df


path = "C:/Users/mathe/Documents/Github-repos/fitna-study/whole text tagger/outputs/dates_tagged_new/0845Maqrizi.Mawaciz.MAB02082022-ara1.completed.dates_tagged"
terms_df = pd.read_csv("C:/Users/mathe/Documents/Github-repos/fitna-study/terms_analysis/terms_resources/terms_list.csv")["Term"].values.tolist()
dates_df = pd.read_csv("C:/Users/mathe/Documents/Github-repos/fitna-study/terms_analysis/terms_resources/dates_list.csv").values.tolist()
out = "C:/Users/mathe/Documents/Github-repos/fitna-study/terms_analysis/0845Maqrizi.Mawaciz.MAB02082022-sectionterms.csv"

with open(path, encoding = "utf-8") as f:
    text = f.read()
    f.close()

terms = terms_df[:]

for row in dates_df:
    for d in range(row[0], row[1]):
        terms.append("@YY" + str(d))

print(terms)

cats = [{'beg': 1, 'end': 100, 'label': 'first-century'}, 
        {'beg': 101, 'end': 357, 'label': 'pre-fatimid'}, 
        {'beg': 358, 'end': 567, 'label': 'fatimid'},
        {'beg': 568, 'end': 648, 'label': 'ayyubid'},
        {'beg': 649, 'end': 783, 'label': 'bahri-mamluk'},
        {'beg': 784, 'end': 900, 'label': 'circassian-mamluk'}]

mapped = pattern_map_cat(text, cats, w_counts = True, map_terms = terms)
mapped.to_csv(out, encoding = "utf-8-sig")




        
            
            
        
    