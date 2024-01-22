# -*- coding: utf-8 -*-

import pandas as pd
import regex as re
from tqdm import tqdm
import os

def results_to_ms_csv(text, search_terms, csv_out_path):
    """Takes list of search terms and text and creates a csv recording how many of each term are in each ms of the text"""
    out_dicts = []

    ms_splits = re.split(r"(ms\d+)", text)    
    for idx, ms_split in enumerate(ms_splits):
        foundit = False
        if len(re.findall(r"ms\d+", ms_split)) == 1:            
            continue
        elif idx+1 < len(ms_splits):
            ms_no = int(ms_splits[idx+1].split("ms")[-1])
            print(ms_no)
            outrow = {"ms": ms_no}
            for term in search_terms:
                outrow[term] = 0
                find_count = len(re.findall(term, ms_split))
                if find_count > 0:
                    foundit = True
                    outrow[term] = find_count
            if foundit:
                out_dicts.append(outrow)

        else:
            continue
    
    df_out = pd.DataFrame(out_dicts)
    df_out.to_csv(csv_out_path, index=False, encoding='utf-8-sig')

def search_openiti(corpus_base_path, metadata_path, out_dir, search_terms, end_date = 900, tag_texts = True, ms_results=True, uri_list = None):
    
    # Make search_terms a list if not a list
    if type(search_terms) == str:
        search_terms = [search_terms]
    
    #Filter the metadata for before date cut off and only primary
    print("fetching directory list")
    metadata = pd.read_csv(metadata_path, sep = "\t")
    metadata = metadata[metadata["status"] == "pri"]
    metadata = metadata[metadata["date"] <= end_date]    
    if uri_list:
        metadata = metadata[metadata["book"].isin(uri_list)]
        if len(metadata) == 0:
            print("Enter a valid URI - you entered {}".format(uri_list))
            exit()
    
    metadata["rel_path"] = corpus_base_path + metadata["local_path"].str.split("\.\./", expand = True)[1]
    location_list = metadata[["version_uri", "rel_path"]].values.tolist()

    results_totals = {}
    for term in search_terms:
        results_totals[term] = 0
    
    outresults = []
    
    if tag_texts:
        tag_root = out_dir + "/tagged_texts/"
        if not os.path.exists(tag_root):
            os.mkdir(tag_root)
    if ms_results:
        csv_root = out_dir + "/ms_csvs/"
        if not os.path.exists(csv_root):
            os.mkdir(csv_root)


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
                    tag = r" @ST" + str(idx) + "@"
                    if tag_texts:
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
                out_path = tag_root + loc[0]
                if tag_texts:
                    with open(out_path, "w", encoding = "utf-8") as f:
                        f.write(text)
                        f.close()
                if ms_results:
                    csv_path = csv_root + loc[0] + ".csv"                    
                    results_to_ms_csv(text, search_terms, csv_path)
        else:
            print("Not found: " + loc[1])
    print(results_totals)
    out_df = pd.DataFrame(outresults)
    out_df.to_csv(out_dir + "/search_results.csv", index = False)

metadata = "D:/Corpus Stats/2023/OpenITI_metadata_2023-1-8.csv"
corpus_base_path = "D:/OpenITI Corpus/corpus_2023_1_8/"
out_dir = "C:/Users/mathe/Documents/Github-repos/fitna-study/search_full_text/search_results_v8"
search_terms = r"الجوان[يى][\r\n\W]"
uri_list = ["0845Maqrizi.Mawaciz"]

search_openiti(corpus_base_path, metadata, out_dir, search_terms, uri_list=uri_list)