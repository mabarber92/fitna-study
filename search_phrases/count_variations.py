# -*- coding: utf-8 -*-

from openiti.helper.ara import normalize_ara_heavy
import pandas as pd
import re
import os
from tqdm import tqdm
from collections import Counter


def capture_phrases(phrase_list, corpus_base_path, metadata_path, end_date = 1000, 
                   non_arabic = r"[^\w\s]|\d|[A-Z]|[a-z]|_", pre_capture = 0, post_capture = 25, meta_field="local_path", 
                   splitter=True, getMs= True):
    # Filter the metadata for before date cut off and only primary
    metadata = pd.read_csv(metadata_path, sep = "\t")
    metadata = metadata[metadata["status"] == "pri"]
    metadata = metadata[metadata["date"] <= end_date]

    # Code to select one book for testing purposes
    # metadata = metadata[metadata["version_uri"] == "0241IbnHanbal.Musnad.Shamela0025794-ara1"]

    
    if splitter:
        metadata["rel_path"] = corpus_base_path + metadata[meta_field].str.split("/master/|\.\./", expand = True, regex=True)[1]
    else:
        metadata["rel_path"] = corpus_base_path + "/" + metadata[meta_field]
    
    location_list = metadata["rel_path"].to_list()
    
    
    

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
        add_length = post_capture - len(norm_phrase.split(" "))
        regexed = regex_start + regex_mid +str(pre_capture) + "}" + norm_phrase + regex_mid + str(add_length) + regex_end
        print(regexed)
        norm_phrase_list.append({"term" : regexed, "count" : 0})

    print(norm_phrase_list)   
    print("\n----------------\n\n")
    
    for location in tqdm(location_list):
        
        if os.path.exists(location):
            with open(location, encoding = "utf-8") as f:
                text = f.read()
                f.close()
            
            # Split off header
            text = re.split(r"#META#Header#End#", text)[-1]
            
            # If getMs split text into milestone chunks and get the clean char positions of ms
            if getMs:
                msLocs = {}
                msSplit = re.split(r"ms(\d+)", text)
                totalSplits = len(msSplit)
                chCount = 0
                
                for idx, split in enumerate(msSplit):
                    if not re.match(r"\d", split) and idx+1 != totalSplits:
                        
                        # Clean out non_arabic
                        cleanSplit = re.sub(non_arabic, " ", split)
                        # Replace multiple spaces
                        cleanSplit = re.sub(r"\s+", " ", cleanSplit)                        
                        # Normalise the text
                        cleanSplit = normalize_ara_heavy(cleanSplit)

                        

                        msId = msSplit[idx+1]

                        chCount = chCount + len(cleanSplit) - 1
                        
                        msLocs[chCount] = msId
            print("...")
            print("Calculated count: {}".format(chCount))
            

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

            print("Cleaned text length: {}".format(len(text)))
            

            for phrase in norm_phrase_list:
                search_result = re.finditer(phrase["term"], text)               
                for result in search_result:
                    if getMs:
                        matchPos = result.start()
                        nearMsCh = min(list(filter((matchPos).__le__, list(msLocs.keys()))))
                        
                        
                        results.append({"phrase": result.group(), "uri": uri, "ms": msLocs[nearMsCh]})
                        
                    else:
                        results.append({"phrase": result.group(), "uri": uri})
        
        print("Number of results: " + str(len(results)))     
    
    # Return a dataframe
    
    return pd.DataFrame(results)
          
def count_token_similarities (results_df, out_csv, total_csv, gram2_csv, gram3_csv, direction = "forward"):
    phrase_list = results_df["phrase"].tolist()
    phrase_length = len(phrase_list[0].split())
    
    # Create a dictionary to recieve the output
    print("creating the terms dictionary...")
    out_pos = {}
    for i in range(0, phrase_length):
        out_pos[i] = []
    
    all_words = []
    grams_2 = []
    grams_3 = []
    
    # Go through each phrase and split into the positions dictionary
    print("Populating the terms dictionary...")
    for phrase in phrase_list:
        tok_list = phrase.split()
        if direction == "forward":
            for pos, tok in enumerate(tok_list):
                out_pos[pos].append(tok)
                # For 2-gram - get a subset based on position - to create shingle
                if pos < phrase_length - 1:                    
                    grams_2.append(" ".join(tok_list[pos:pos+2]))
                    
                if pos < phrase_length - 2:                    
                    grams_3.append(" ".join(tok_list[pos:pos+3]))
                    
                    
        if direction == "backward":
            for pos, tok in reversed(enumerate(tok_list)):
                out_pos[pos].append(tok)
                # For 2-gram - get a subset based on position - to create shingle
                if pos < phrase_length - 1:
                    grams_2.append(" ".join(tok_list[pos:pos+2]))
                if pos < phrase_length - 2:                    
                    grams_3.append(" ".join(tok_list[pos:pos+3]))
        
        # Create a list of all words
        all_words.extend(tok_list)
       
    
    # Count and log the variants at each position
    print("Counting the term variations at each position")    
    output = []
    for pos in out_pos.keys():
        full_list = out_pos[pos]
        counted = Counter(full_list)
        for key in counted.keys():            
            output.append({"pos": pos, "word" : key, "count" : counted[key]})
    
    pd.DataFrame(output).to_csv(out_csv, index=False, encoding = 'utf-8-sig')
    
    # Produce Total Counts
    print("counting total words")
    total_counts = []
    total_counted = Counter(all_words)
    for key in total_counted.keys():
        total_counts.append({"word" : key, "count" : total_counted[key]})
    
    total_df = pd.DataFrame(total_counts)
    total_df = total_df.sort_values(["count"], ascending = False)
    total_df.to_csv(total_csv, index=False, encoding = 'utf-8-sig')
    
    # Produce 2-gram Counts
    print("counting total 2-grams")
    grams_2_count = []
    grams2_counted = Counter(grams_2)
    for key in grams2_counted.keys():
        grams_2_count.append({"word" : key, "count" : grams2_counted[key]})
    
    gram_2_df = pd.DataFrame(grams_2_count)
    gram_2_df = gram_2_df.sort_values(["count"], ascending = False)
    gram_2_df.to_csv(gram2_csv, index=False, encoding = 'utf-8-sig')
    
    # Produce 3-gram Counts
    print("counting total 3-grams")
    grams_3_count = []
    grams3_counted = Counter(grams_3)
    for key in grams3_counted.keys():
        grams_3_count.append({"word" : key, "count" : grams3_counted[key]})
    
    gram_3_df = pd.DataFrame(grams_3_count)
    gram_3_df = gram_3_df.sort_values(["count"], ascending = False)
    gram_3_df.to_csv(gram3_csv, index=False, encoding = 'utf-8-sig')
    
# phrases_csv = "C:/Users/mathe/Documents/Github-repos/fitna-study/search_phrases/Yusuf_focused_terms/phrase_queries.csv"  
# phrase_list = pd.read_csv(phrases_csv)["term"].tolist()
# phrase_list = ["اشتد الغلاء", "وعم الغلاء", "القحط المفرط", "الغلاء المفرط", "الغلاء والقحط", "اشتداد الغلاء", "امتد الغلاء", "الغلاء قد اشتد", "لم تبق اقوات", ]
phrase_list = ["[بفل]?موسى"]

corpus_base_path = "D:/OpenITI Corpus/corpus_2022_1_6/"
metadata_path = "D:/Corpus Stats/2022/OpenITI_metadata_2022-1-6.csv"
out = "Moses_results/variation_counts1.csv"
total = "Moses_results/total_counts1.csv"
gram2 = "Moses_results/total_2grams.csv"
gram3 = "Moses_results/total_3grams.csv"
results_path = "Moses_results/results-ms-corrected.csv"

metadata_path2 = "D:/OpenITI Corpus/9001AH-master/OpenITI-9001AH_metadata_2020-2-3.csv"
corpus_base_path2 = "D:/OpenITI Corpus/9001AH-master/"

results = capture_phrases(phrase_list, corpus_base_path, metadata_path, pre_capture = 30, post_capture = 30)
results2 = capture_phrases(phrase_list, corpus_base_path2, metadata_path2, pre_capture = 30, post_capture = 30, meta_field="url", splitter=False)
results = pd.concat([results, results2])
results.to_csv(results_path, encoding = "utf-8-sig", index = False)
# count_token_similarities(results, out, total, gram2, gram3)