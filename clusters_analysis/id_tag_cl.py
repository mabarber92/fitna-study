# -*- coding: utf-8 -*-
"""
Created on Tue Feb  8 09:41:30 2022

@author: mathe
"""

import pandas as pd
from tqdm import tqdm
import pyarrow.parquet as pq
import os
import json
import math
pd.options.mode.chained_assignment = None

def id_clusters_text_tag(clusters_in_listed, book_dict, cluster_dict, parquet_path, meta_path, csv_out, corpus_path, tagged_out, check_ms = True, tag = True, cluster_cap = 500):
    """"""
    # Load in required data
    metadata = pd.read_csv(meta_path, sep= "\t")[["id", "local_path", "book"]]
    os.chdir(parquet_path)
    df_out = pd.DataFrame()
    
    # Use json to augment full cluster list if check_ms is True. This allows us to identify any clusters associated with the same milestones that are not in the list. This only goes to a depth of one (that is clusters associated with the first set of clusters-milestones - otherwise we get runaway and connections to large parts of the corpus)
    if check_ms:
        print("\nFinding related milestones and expanding to include relevant clusters\n")
        new_clusters = []
        for cluster in tqdm(clusters_in_listed):
            book_ms_list = cluster_dict[str(cluster)]
            for book in book_ms_list:
                bid = book.split(".")[0]
                new_clusters.extend(book_dict[bid][book])
        new_clusters = list(dict.fromkeys(new_clusters))
        for cluster in tqdm(clusters_in_listed):
            if cluster in new_clusters:                
                new_clusters.remove(cluster)

    
    # Populate dataframe with only selected clusters
    print("\nFetching data from the clusters\n")
    for root, dirs, files in os.walk(".", topdown=False):
        for name in tqdm(files):
            pq_path = os.path.join(root, name)            
            data = pq.read_table(pq_path).to_pandas()[["cluster", "size", "id", "text", "series"]]
            # Filtering out enormous unhelpful clusters
            data = data.loc[data["size"] <= cluster_cap]
            ## Filter using the list of clusters
            filtered_data = data[data["cluster"].isin(clusters_in_listed)]
            filtered_data["from_input"] = True
            df_out = pd.concat([df_out, filtered_data])
            
            ## If set, find any new clusters associated with the milestones associated with the clusters
            if check_ms:                
                other_clusters = data[data["cluster"].isin(new_clusters)]
                other_clusters["from_input"] = False
                df_out = pd.concat([df_out, other_clusters]).drop_duplicates()
            #     clusters_in_listed.extend(new_clusters["cluster"].tolist())
    
    # Add metadata to the output
    df_out["series"] = df_out["series"].str.split("-", expand = True)[0]
    
    metadata = metadata.rename(columns = {"id": "series"})
    df_out = pd.merge(df_out, metadata, how = "inner", on ="series")
    
    # Get the paths of all unique texts in the df - fetch the texts and tag the milestones listed in the df with the relevant clusters
    if tag: 
        print("\nInserting tags into texts related to the clusters\n")
        path_list = df_out.loc[df_out["from_input"] == True]["local_path"].drop_duplicates().tolist()
        print(path_list)
        for path in tqdm(path_list):
            data_subset = df_out.loc[df_out["local_path"] == path]["id"].drop_duplicates().tolist()
            if type(path) == str:
                path_in = corpus_path + "/" + path.split("../")[-1]
                if os.path.exists(path_in):
                    with open(path_in, encoding = "utf-8") as f:
                        text = f.read()
                        f.close()
                    book = data_subset[0].split(".")[0]
                    for ms_id in data_subset:
                        ms = ms_id.split(".")[-1]
                        clusters = book_dict[book][ms_id]
                        tag = " " + ms
                        for cluster in clusters:
                            tag = tag + " @cl@" + str(cluster) + "@ "
                        text = text.replace(ms, tag)
                    out_path = tagged_out + "/" + path.split("/")[-1] + ".cl-tagged"
                    with open(out_path, "w", encoding = "utf-8") as f:
                        f.write(text)
                        f.close()
                else:
                    print("\nPath: " + path_in + "does not exist - check your specified corpus folder\n")
            else:
                print("\nNo path value for this work, value given: " + path + "\n")
    
    # Sort the values so clusters are all together and remove the local_path column
    df_out = df_out.drop(["local_path", "series"], axis=1)
    sort_vals = ["cluster", "from_input", "book"]
    df_out = df_out.sort_values(by = sort_vals, ascending = True)
    
    df_len = len(df_out)
    if df_len > 200:
        out_dir = csv_out + "/"
        if not os.path.exists(out_dir):
            os.mkdir(out_dir)
        sheet_no = math.ceil(df_len/200)
        for i in range(1, sheet_no+1):
            row_count = (i*200)
            end = row_count -1
            start = row_count-200
            df_slice = df_out[start: end]
            csv_path = out_dir + "rows-" + str(start) + "-" + str(end) + ".csv"
            df_slice.to_csv(csv_path, index=False, encoding = "utf-8-sig")
        input_only = df_out[df_out["from_input"]== True]
        input_only.to_csv(out_dir + "input-only.csv", index=False, encoding = "utf-8-sig")
        
    else:
        df_out.to_csv(csv_out + ".csv", index=False, encoding = "utf-8-sig")


parquets = "D:/Corpus Stats/2021/Cluster data/Oct_2021/parquet/"
# clusters_in = [85899445345, 85899429280]
metadata = "D:/Corpus Stats/2021/OpenITI_metadata_2021-2-5_merged_wNoor.csv"
out = "C:/Users/mathe/Documents/Github-repos/fitna-study/clusters_analysis/"

book_json = "D:/Corpus Stats/2021/Cluster data/Oct_2021/for_ms_app/books_dict.json"
cluster_json = "D:/Corpus Stats/2021/Cluster data/Oct_2021/for_ms_app/clusters.json"

out_path = "C:/Users/mathe/Documents/Github-repos/fitna-study/clusters_analysis/texts_cl_tagged/"
corpus_path = "D:/OpenITI Corpus/corpus_10_21"


with open(book_json) as f:
    book_dict = json.load(f)
    f.close()
    
with open(cluster_json) as f:
    cluster_dict = json.load(f)
    f.close()

# id_clusters_text_tag(clusters_in, book_dict, cluster_dict, parquets, metadata, out, corpus_path, out_path)

clusters_files = "C:/Users/mathe/Documents/Github-repos/fitna-study/clusters_analysis/labelled_lists"

for root, dirs, files in os.walk(clusters_files, topdown=False):
        for name in files:
            print("Working with: " + name + "\n")
            print("Do you wish to proceed with this file (y/n)")
            proceed = input()
            if proceed == 'n':
                continue
            if proceed == 'y':
                csv_path = os.path.join(root, name) 
                non_ext = name.split(".")[0]
                final_out_texts = out_path + "/" + non_ext + "/"
                if not os.path.exists(final_out_texts):
                    os.mkdir(final_out_texts)
                clusters_in = pd.read_csv(csv_path)["cluster"].astype('Int64').tolist()
                
                final_out = out + "/" + non_ext
                id_clusters_text_tag(clusters_in, book_dict, cluster_dict, parquets, metadata, final_out, corpus_path, final_out_texts, tag = False)
