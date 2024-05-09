# -*- coding: utf-8 -*-
"""
Created on Wed Jun 16 14:51:43 2021

@author: mathe
"""
import re
import pandas as pd
from tqdm import tqdm
import os
import pathlib

def pattern_map_cat(text, date_cats = [], add_terms = None, on = "head", tops = None, w_counts = False, char_counts = False, map_terms = None):
    """ Takes date-range dictionary of {'beg': 0, 'end': 358, 'label': 'pre-Fatimid} """
    out = []
    columns = ["section"]
    
  
    if on == "head":
        splits = re.split(r"###\s", text)
    if on == "ms":
        splits = re.split(r"ms\d+", text)
    
    
    if w_counts:
        columns.append("st_pos")
        columns.append("mid_pos")
    
    if char_counts:
        columns.append("st_pos")
        columns.append("mid_pos")
        
    for label in date_cats:
        columns.append(label["label"])
    
    if add_terms is not None:
        columns.extend(add_terms)
        
    if tops:
        columns.append("Topic_id")
    
    if map_terms is not None:
        terms_copy = map_terms[:]
        for term in map_terms:
            count = len(re.findall(term, text))
            if count == 0:
                terms_copy.remove(term)
        columns.extend(terms_copy)
        
    word_char_counter = 0
 
 
    
    for idx, split in enumerate(tqdm(splits)):
        temp = [idx + 1]
        if w_counts:
            temp.append(word_char_counter)
            sec_length = len(re.split(r"\s", split))
            temp.append(word_char_counter + (sec_length/2))
            word_char_counter = word_char_counter + sec_length
        if char_counts:
            temp.append(word_char_counter)
            sec_length = len(split)
            temp.append(word_char_counter + (sec_length/2))
            word_char_counter = word_char_counter + sec_length
            
        ### Iterate through date-ranges dict
        for item in date_cats:
            type_count = 0
            for i in range(item['beg'], item['end']):
                regex = r"@YY" + str(i).zfill(3)
                type_count = type_count + len(re.findall(regex, split))
            temp.append(type_count)
                
        if add_terms is not None:
            for term in add_terms:            
                count = len(re.findall(term, split))
                temp.append(count)
        if tops is not None:            
            topic = re.findall(tops, split)
            if len(topic) >= 1:
                temp.append(topic[0])
            else:
                temp.append("None")
        for term in terms_copy:            
            count = len(re.findall(term, split))
            temp.append(count)
        out.append(temp)
    

            
        
    
    out_df = pd.DataFrame(out, columns = columns)
    
    return out_df


# in_path = "C:/Users/mathe/Documents/Github-repos/fitna-study/whole text tagger/outputs/dates_tagged_new"
# out_path = "C:/Users/mathe/Documents/Github-repos/fitna-study/dates_analysis/mappings_mamluk_split"


# cats = [{'beg': 1, 'end': 100, 'label': 'first-century'}, 
#         {'beg': 101, 'end': 357, 'label': 'pre-fatimid'}, 
#         {'beg': 358, 'end': 567, 'label': 'fatimid'},
#         {'beg': 568, 'end': 648, 'label': 'ayyubid'},
#         {'beg': 649, 'end': 783, 'label': 'bahri-mamluk'},
#         {'beg': 784, 'end': 900, 'label': 'circassian-mamluk'}]


# for root, dirs, files in os.walk(in_path, topdown=False):
#     for name in tqdm(files):
#         print(name)            
#         text_path = os.path.abspath(os.path.join(root, name))
#         section_path = out_path + "/sections/"
#         ms_path = out_path + "/ms/"
#         if not os.path.exists(section_path):
#             pathlib.Path(section_path).mkdir(parents=True, exist_ok=True)
#         if not os.path.exists(ms_path):
#             pathlib.Path(ms_path).mkdir(parents=True, exist_ok=True)
#         section_path = out_path + "/sections/" + name + ".s_mapped.csv"
#         ms_path = out_path + "/ms/" + name + ".ms_mapped.csv"
        
#         with open(text_path, encoding = "utf-8") as f:
#             text = f.read()
#             f.close()
            
#         section_mappings = pattern_map_cat(text, date_cats = cats, tops = False, w_counts=True, char_counts = False)
#         section_mappings.to_csv(section_path)
        
#         ms_mappings = pattern_map_cat(text, date_cats = cats, on="ms", tops = False, w_counts=True, char_counts = False)
#         ms_mappings.to_csv(ms_path)
        
    