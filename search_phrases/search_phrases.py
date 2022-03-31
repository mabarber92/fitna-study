# -*- coding: utf-8 -*-

from openiti.helper.ara import normalize_ara_heavy
import pandas as pd
import re
import os
from tqdm import tqdm

def search_phrases(phrase_list, corpus_base_path, metadata_path, sum_out, book_out, end_date = 1000, 
                   non_arabic = r"[^\w\s]|\d|[A-Z]|[a-z]"):
    # Filter the metadata for before date cut off and only primary
    metadata = pd.read_csv(metadata_path, sep = "\t")
    metadata = metadata[metadata["status"] == "pri"]
    metadata = metadata[metadata["date"] <= end_date]
    metadata["rel_path"] = corpus_base_path + metadata["local_path"].str.split("/master/", expand = True)[1]
    location_list = metadata["rel_path"].to_list()
    
    
    norm_phrase_list = []
    text_counts = []
    
    for phrase in phrase_list:
        norm_phrase_list.append({"term" : normalize_ara_heavy(phrase), "count" : 0})
        
    
    for location in tqdm(location_list):
        
        if os.path.exists(location):
            with open(location, encoding = "utf-8") as f:
                text = f.read()
                f.close()
            
            # Get URI for output
            uri = location.split("/")[-1]
            
            # Replace non-Arabic characters with a space
            text = re.sub(non_arabic, " ", text)
            # Remove new lines
            text = re.sub("\n", " ", text)
            # Replace multiple spaces
            text = re.sub(r"\s+", " ", text)
            
            # Normalise the text
            text = normalize_ara_heavy(text)
            
            text_total = 0
            
            for phrase in norm_phrase_list:
                count = len(re.findall(phrase["term"], text))
                if count == 0:
                    continue
                # Logging data for term totals
                phrase["count"] = phrase["count"] + count
                
                # Logging data for individual book
                text_counts.append({"book": uri, "phrase": phrase["term"], "count": count})
                text_total = text_total + count
           
            # Logging total found for all phrases 
            if text_total != 0:
                text_counts.append({"book": uri, "phrase" : "All phrases", "count": text_total})
    
    # Write out the data into dataframes
    
    pd.DataFrame(norm_phrase_list).to_csv(sum_out, index = False, encoding = "utf-8-sig")
    pd.DataFrame(text_counts).to_csv(book_out, index = False, encoding = "utf-8-sig")
          
        
        
    
phrases_csv = "C:/Users/mathe/Documents/Github-repos/fitna-study/search_phrases/phrases_list_1.csv"  
phrase_list = pd.read_csv(phrases_csv)["terms"].tolist()
print(phrase_list)
corpus_base_path = "D:/OpenITI Corpus/latest_corpus_02_21/"
metadata_path = "D:/Corpus Stats/2021/OpenITI_metadata_2021-2-5.csv"
sum_out = "phrase_list1_sum.csv"
book_out = "phrase_list1_book.csv"

search_phrases(phrase_list, corpus_base_path, metadata_path, sum_out, book_out)