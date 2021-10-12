# -*- coding: utf-8 -*-
"""
Created on Sun Oct 10 11:20:19 2021

@author: mathe
"""

# Need to strip out page nos, puntuation etc.

import re


def split_date_freq(text, n_grams = [1, 2], exc_freq = 5):
    "Function that gets specified and counted ngrams"
    
    # Split text by section - create list for output
    maintext = re.split("#META#Header#End#", text)[1]
    section_list = re.split("###", maintext)
    list_out = []
    excs_out = []
    grams_list = []
    for seq, section in enumerate(section_list):
        dict_item = {}
    # Get title and level
        print(".", sep="")
        title = re.findall(r"\s\|+\s.*\n", section)
        if len(title) == 0:
            continue
        level = len(re.findall(r"\s(\|+)\s", title[0])[0])
        dict_item["seq"] = seq
        dict_item["title"] = title
        dict_item["level"] = level
        
        dates = re.findall(r"@YY(\d{3})", section)
        if len(dates) >= 1:
            dates = dates.sort()
            dict_item["dates"] = dates
        else:
            dict_item["dates"] = "None"
        
        # Remove all puntuation, latin script chars and numbers
        section = re.sub(r"[a-z]|[A-Z]|[.,:;\d@؟\",!#\]\[-]", "", section)
        
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
            grams_list.append(dict_name)  
            
            
        # Write dict to list
        list_out.append(dict_item)
    return list_out, excs_out, grams_list

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
                            
                    
        
        
path = "C:/Users/mathe/Documents/Kitab project/Big corpus datasets/date_tagged_corpus/15_03/dated/0845Maqrizi.Mawaciz.Shamela0011566-ara1.completed"

with open(path, encoding = "utf-8") as f:
    text = f.read()
    f.close()

out, exc_out = split_date_freq(text)
# Split text into sections

# Get section title - pass to dict

# Get section level 

# Get dates - sort in order and add to dict - sub out these tags to remove from freq list

# Get word frequencies, store as list of dicts and pass to dict
    # Convert to list then create dict and second list to get one of each - look through subsequent list and count in the first list

# Get bi-gram frequencies as well - shingled - findall "/s/w+/s"

# Pass everything to large list

# In larger list, sort to see most common combinations