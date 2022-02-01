# -*- coding: utf-8 -*-
"""
Created on Tue Jan 18 15:32:40 2022

@author: mathe
"""

import pandas as pd
import re
import pyarrow.parquet as pq
import os
from tqdm import tqdm

def cluster_search_string(regex, add_regex, parquet_path, meta_path, csv_out, max_date = 900, cluster_cap = 500):
    """Searches parquet files directly to identify clusters with specified search path.
    Outputs are split based on the count of terms found in each milestone string. If you 
    want to identify terms that appear alongside the priority search terms in 'regex' these
    can be added using 'add_regex' terms in this field will only be identified in the string
    if terms have already been identified in the string for the primary 'regex'. The output
    csv provides counts for the primary term and the additional terms. Splitting outputs is
    determined by a sum of the count of the primary and 'add_regex', if add_regex is specified.
    That is, -above-1-match.csv contains strings that only match the primary regex once but also
    match an additional term. max_date filters the final output using metadata to remove any hits for books before 
    the specified death date. cluster_cap specifies maximum size of the clusters to search (default setting of 500 
    to avoid super-massive clusters)
    """
    out_list_above_1 = []
    out_list_1 = []
    os.chdir(parquet_path)
    for root, dirs, files in os.walk(".", topdown=False):
        for name in tqdm(files):
            pq_path = os.path.join(root, name)            
            data = pq.read_table(pq_path).to_pandas()[["cluster", "size", "id", "text", "series"]].values.tolist()
            for cluster in data:
                if cluster[1] > cluster_cap:
                    continue
                if re.search(regex, cluster[-2]):
                    tagged, count = re.subn(regex, r"@\1@", cluster[-2])
                    if add_regex is not None:
                        tagged, count2 = re.subn(add_regex, r"@\1@", tagged) 
                    row = cluster[:-2]
                    bid = cluster[-1].split("-")[0]
                    row.append(bid) 
                    row.append(tagged)                                       
                    row.append(count)
                    if add_regex is not None:
                        row.append(count2)
                        count = count + count2
                        row.append(count)                    
                    if count == 1:
                        out_list_1.append(row)
                    else:
                        out_list_above_1.append(row)
            
                    
    columns =  ["cluster", "size", "id", "series", "text", "primary_match_count"]
    sort_vals = ["cluster", "primary_match_count"]
    if regex is not None:
        columns.extend(["additional_terms", "total_count"])
        sort_vals = ["cluster", "total_count"]
    df_1 = pd.DataFrame(out_list_1, columns = columns)
    df_above_1 = pd.DataFrame(out_list_above_1, columns = columns)
    
    
    
    # Add book URI to make easier to read outputs
    meta_df = pd.read_csv(meta_path, sep="\t")[["id", "book", "date"]]
    meta_df = meta_df.rename(columns = {"id": "series"})
    df_1 = pd.merge(df_1, meta_df, how = "inner", on ="series")
    df_above_1 = pd.merge(df_above_1, meta_df, how = "inner", on ="series")
    
    
    # Applying the date filter to output
    df_1 = df_1[(df_1["date"] <= max_date)]
    df_above_1 = df_above_1[(df_above_1["date"] <= max_date)]
    df_1 = df_1.drop(columns = ["series", "date"])
    df_above_1 = df_above_1.drop(columns = ["series", "date"])
    
    # Sort the dataframes
    df_above_1 = df_above_1.sort_values(by = sort_vals, ascending = False)
    df_1 = df_1.sort_values(by = ["cluster"], ascending = False)
    
    # Output final results
    print("total filtered matches of 1: " + str(len(df_1)))
    print("total filtered matches over 1: " + str(len(df_above_1)))
    
    # Write out the output
    df_1.to_csv(csv_out + "-1-match.csv", index = False, encoding = 'utf-8-sig')
    df_above_1.to_csv(csv_out + "-above-1-match.csv", index = False, encoding = 'utf-8-sig')
    
    
path = "D:/Corpus Stats/2021/Cluster data/Oct_2021/parquet/"
test_path = "D:/Corpus Stats/2021/Cluster data/Oct_2021/test"
meta_path = "D:/Corpus Stats/2021/OpenITI_metadata_2021-2-5_merged_wNoor.csv"
out = "C:/Users/mathe/Documents/Github-repos/fitna-study/clusters_analysis/famine-terms"

regex = r"([^شد]غل[وا][ء\sا]|قحط\s)"
add_regex = "(وباء|[اأ]كل|[^شر]ج[وا]ع)"
cluster_search_string(regex, add_regex, path, meta_path, out)



            