# -*- coding: utf-8 -*-
"""
Created on Tue Oct 25 13:34:18 2022

@author: mathe
"""

from openiti.helper.ara import normalize_ara_heavy
import pandas as pd
import re
import os
from tqdm import tqdm
from collections import Counter

def find_surrounding_toks(phrase_list, corpus_base_path, metadata_path, out_csv, end_date = 1000, 
                   non_arabic = r"[^\w\s]|\d|[A-Z]|[a-z]|_", pre_capture = 1, post_capture = 0, meta_field="local_path", 
                   debug=False, splitter=True):
    # Filter the metadata for before date cut off and only primary
    metadata = pd.read_csv(metadata_path, sep = "\t")
    metadata = metadata[metadata["status"] == "pri"]
    metadata = metadata[metadata["date"] <= end_date]
    if splitter:
        metadata["rel_path"] = corpus_base_path + metadata[meta_field].str.split("/master/", expand = True)[1]
    else:
        metadata["rel_path"] = corpus_base_path + "/" + metadata[meta_field]
    location_list = metadata["rel_path"].to_list()
    if debug:        
        print(location_list)
    
    norm_phrase_list = []
    results = []
    
    # For the singling and counting it is important that we capture the same length phrase regardless 
    # of the length of the input string. So we determine the number of tokens captured by the regex
    # after the phrase by deducting the token count of  the phrase from the max_capture parameter
    # the number of tokens captured prior to the phrase remains fixed
    regex_start = "("
    regex_mid = "\s(\w+\s){" 
    regex_end = "})"
    
    for phrase in phrase_list:
        norm_phrase = normalize_ara_heavy(phrase)
        
        regexed = regex_start + regex_mid +str(pre_capture) + "}" + norm_phrase + regex_mid + str(post_capture) + regex_end
        print(regexed)
        norm_phrase_list.append({"term" : regexed, "count" : 0})
        
    print("\n----------------\n\n")
    
    for location in tqdm(location_list):
        
        if os.path.exists(location):
            with open(location, encoding = "utf-8") as f:
                text = f.read()
                f.close()
            
            
            # Replace non-Arabic characters with a space
            text = re.sub(non_arabic, " ", text)
            # Remove new lines
            text = re.sub("\n", " ", text)
            # Replace multiple spaces
            text = re.sub(r"\s+", " ", text)
            
            # Normalise the text
            text = normalize_ara_heavy(text)
            

            for phrase in norm_phrase_list:
                search_result = re.findall(phrase["term"], text)
                for result in search_result:
                    results.append(result[0])
                
    # Use counter to condense the phrases and output to df
    
    phrase_count = []
    phrase_counted = Counter(results)
    for key in phrase_counted.keys():
        phrase_count.append({"word" : key, "count" : phrase_counted[key]})
    
    phrase_df = pd.DataFrame(phrase_count)
    phrase_df = phrase_df.sort_values(["count"], ascending = False)
    phrase_df.to_csv(out_csv, index=False, encoding = 'utf-8-sig')
    
corpus_base_path = "D:/OpenITI Corpus/9001AH-master"
metadata_path = "D:/OpenITI Corpus/9001AH-master/OpenITI-9001AH_metadata_2020-2-3.csv"
out = "Yusuf_search/Ismaili_sub_corpus/search_results.csv"
phrase_list = [".?يوسف"]

find_surrounding_toks(phrase_list, corpus_base_path, metadata_path, out, meta_field="url", debug=True, splitter=False)
