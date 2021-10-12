# -*- coding: utf-8 -*-
"""
Created on Wed Jun 16 14:51:43 2021

@author: mathe
"""
import re
import pandas as pd

def pattern_map(text, terms, on = "head", tops = False, w_counts = False):
    if on == "head":
        splits = re.split(r"###\s", text)
    if on == "ms":
        splits = re.split(r"ms\d+", text)
    
    out = []
    columns = ["section"]
    if w_counts:
        columns.append("st_pos")
        columns.append("mid_pos")
    columns.extend(terms)
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
            
            
            
                
        for term in terms:            
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


path = "C:/Users/mathe/Documents/Kitab project/Big corpus datasets/date_tagged_corpus/whole text tagger/outputs/0845Maqrizi.Mawaciz.Shamela0011566-ara1.date_tagged"

with open(path, encoding = "utf-8") as f:
    text = f.read()
    f.close()

mapped = pattern_map(text, terms = ["باب العزم"], tops = False, w_counts = True)

        
            
            
        
    