# -*- coding: utf-8 -*-
"""
Created on Sun Oct 10 11:20:19 2021

@author: mathe
"""

# Need to strip out page nos, puntuation etc.

import re
import os
from tqdm import tqdm
import json


def split_date_freq(text, n_grams = [2, 3], exc_freq = 5):
    "Function that gets specified and counted ngrams"
    
    # Split text by section - create list for output
    maintext = re.split("#META#Header#End#", text)[1]
    section_list = re.split("###", maintext)
    list_out = []
    excs_out = []
    grams_list = []
    # Write out gram headers for later
    for n_gram in n_grams:
        name = "freqs_" + str(n_gram) + "gram"
        grams_list.append(name)
    
    word_counter = 0
    
    for seq, section in enumerate(tqdm(section_list)):
            dict_item = {}
    # Get title and level
        
            title = re.findall(r"\s\|+\s.*\n", section)
            if len(title) == 0:
                continue
            level = len(re.findall(r"\s(\|+)\s", title[0])[0])
            dict_item["seq"] = seq
            dict_item["title"] = title
            dict_item["level"] = level
            
            
            dict_item["st_pos"] = word_counter
            sec_length = len(re.split(r"\s", section))
            dict_item["mid_pos"] = word_counter + (sec_length/2)
            word_counter = word_counter + sec_length
            
            dates = re.findall(r"@YY(\d{3})", section)
            
            if len(dates) >= 1:
                dates.sort(key = int)
                
                dict_item["dates"] = dates
            else:
                dict_item["dates"] = "None"
                
            
            # Remove all puntuation, latin script chars and numbers
            section = re.sub(r"[a-z]|[A-Z]|[.,:;\d@؟\",!#\]\[-~]", "", section)
            
            # Tokenize and count according to specified ngram sequences (using shingling method)
            tokenized = section.split()
           
            for n_gram in n_grams:
                shingled = [tokenized[i:i+n_gram] for i in range(len(tokenized)-2+n_gram)]
                joined = []
                if n_gram >= 2:
                    
                    for item in shingled:
                        joined.append(" ".join(item))
                else:
                     for item in shingled:
                        joined.append(item[0])
                
                
                
                ## Now only get unique and count freqs
                unique = list(set(joined))
                freqs = []
                for gram in unique:
                    freq = joined.count(gram)
                    new_item = {}
                    new_item[gram] = freq
                    freqs.append(new_item)
                    
                    if freq >= exc_freq:
                        exc_item = dict_item.copy()
                        exc_item[gram] = freq
                        excs_out.append(exc_item)
                
                dict_name = "freqs_" + str(n_gram) + "gram"
                dict_item[dict_name] = freqs
            
            list_out.append(dict_item)
 
            
        # Write dict to list
            
    return list_out, excs_out, grams_list


def comp_dates(seq_list):
    seq_copy = seq_list[:]
    out = []
    for no, seq in enumerate(tqdm(seq_list)):
        seq_copy.remove(seq)
        dates = seq["dates"]
        
        
        if dates == "None":
            continue
        else:
            if "000" in dates:
                dates.remove("000")
            out_dict = {}            
            cluster = []
            f_dates = []
            for copied in seq_copy:
                match = False
                m_count = 0
                for date in dates:
                    if date in copied["dates"]:
                        match = True
                        m_count = m_count + 1
                    if match:
                        cluster.append({"section" : [copied["seq"], copied["title"], copied["dates"]], "match_count" : m_count})
                        f_dates.extend(copied["dates"])
            if len(cluster) >= 1:
                f_dates.extend(seq["dates"])
                f_dates = list(dict.fromkeys(f_dates))
                out_dict["cluster"] = no
                out_dict["sections"] = len(cluster)
                out_dict["all_dates"] = f_dates
                cluster.append([seq["seq"], seq["title"], seq["dates"]])
                out_dict["sections"] = cluster
                out.append(out_dict)
    print(str(len(out)) + " date clusters found")
    return out    
                
# New variant - loop through adding edges to nx graph with weights corresponding
# to number of matches between each section. Then run community detection on sub
# network graph - how will this take account of shared date combinations - weight 
# doesn't know the actual dates        
                        

def compare_freqs(seq_list, grams_list, thresh, on_dates = False):
    seq_copy = seq_list[:]
    for seq in seq_list:
        for title in grams_list:
            freq_list = seq[grams_list]
            for item in freq_list:
                match_count = 0
                gram = item.key()
                seq_copy.remove(seq)
                for item_comp in seq_copy:
                    if item_copy[title].has_key(gram):
                        match_count = match_count + 1
                        # INSTEAD FOR MATCH COUNT USE SUM OF FREQUENCIES IN COMPARED DOCUMENTS
                        # Need a way to count cumulatively - same ngrams between multiple sections
                            
                    
        
        
path = "C:/Users/mathe/Documents/Github-repos/fitna-study/whole text tagger/outputs/dates_tagged/0821Qalqashandi.SubhAcsha.Shamela0009429-ara1.dates_tagged"
path_out = "C:/Users/mathe/Documents/Github-repos/fitna-study/dates_analysis/qal_date_clusters/dated_splits_2_3_grams.json"

with open(path, encoding = "utf-8") as f:
    text = f.read()
    f.close()
    
dict_list, excs_out, grams_list = split_date_freq(text)

json_out = json.dumps(dict_list, indent = 2)
json_out.encode('ascii').decode('unicode-escape')

with open(path_out, "w", encoding = "utf-8") as f:
    f.write(json_out)
    f.close()



# out, exc_out, grams_out = split_date_freq(text)
# Split text into sections

# Get section title - pass to dict

# Get section level 

# Get dates - sort in order and add to dict - sub out these tags to remove from freq list

# Get word frequencies, store as list of dicts and pass to dict
    # Convert to list then create dict and second list to get one of each - look through subsequent list and count in the first list

# Get bi-gram frequencies as well - shingled - findall "/s/w+/s"

# Pass everything to large list

# In larger list, sort to see most common combinations