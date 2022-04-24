# -*- coding: utf-8 -*-

import pandas as pd
import regex as re
from tqdm import tqdm
import os

def search_openiti(corpus_base_path, metadata_path, out_dir, search_terms, end_date = 900):
    
    # Make search_terms a list if not a list
    if type(search_terms) == str:
        search_terms = [search_terms]
    
    #Filter the metadata for before date cut off and only primary
    print("fetching directory list")
    metadata = pd.read_csv(metadata_path, sep = "\t")
    metadata = metadata[metadata["status"] == "pri"]
    metadata = metadata[metadata["date"] <= end_date]
    metadata["rel_path"] = corpus_base_path + metadata["local_path"].str.split("\.\./", expand = True)[1]
    location_list = metadata[["version_uri", "rel_path"]].values.tolist()

    results_totals = {}
    for term in search_terms:
        results_totals[term] = 0
    
    outresults = []
    
    for loc in tqdm(location_list):
        if os.path.exists(loc[1]):
            with open(loc[1], encoding = "utf-8") as f:
                text = f.read()
                f.close()
            firstfind = True
            foundit = False
            result_dict = {}
            for idx, term in enumerate(search_terms):
                count = len(re.findall(term, text))
                if count > 0:
                    results_totals[term] = results_totals[term] + count
                    tag = r"\s@ST" + str(idx) + "@"
                    new_regex = r"(\s\S*{})".format(term)
                    replace = r"{}\1".format(tag)
                    text = re.sub(new_regex, replace, text)
                    if firstfind:
                        result_dict["text"] = loc[0]
                        for term in search_terms:
                            result_dict[tag] = 0
                            firstfind = False
                    result_dict[tag] = count
                    foundit = True
            if foundit:
                outresults.append(result_dict)
                out_path = out_dir + "/" + loc[0]
                with open(out_path, "w", encoding = "utf-8") as f:
                    f.write(text)
                    f.close()
        else:
            print("Not found: " + loc[1])
    print(results_totals)
    out_df = pd.DataFrame(outresults)
    out_df.to_csv(out_dir + "/search_results.csv", index = False)

metadata = "D:/Corpus Stats/2021/OpenITI_metadata_2021-2-5_merged_wNoor.csv"
corpus_base_path = "D:/OpenITI Corpus/corpus_10_21/"
out_dir = "C:/Users/mathe/Documents/Github-repos/fitna-study/search_full_text/search_results"
search_terms = r"الجوان[يى][\r\n\W]"

search_openiti(corpus_base_path, metadata, out_dir, search_terms)