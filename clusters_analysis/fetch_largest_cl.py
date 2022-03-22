# -*- coding: utf-8 -*-
"""
Created on Fri Feb 11 15:44:16 2022

@author: mathe
"""

from tqdm import tqdm
import pyarrow.parquet as pq
import os
import pandas as pd
import re


def fetch_largest(path):
    os.chdir(path)
    for root, dirs, files in os.walk(".", topdown=False):
        out_df = pd.DataFrame()
        for name in tqdm(files):
            pq_path = os.path.join(root, name)            
            data = pq.read_table(pq_path).to_pandas()[["cluster", "size"]]
            out_df = pd.concat([out_df, data])
    
    maxi = out_df["size"].max()
    return maxi, out_df


def count_corpus_ms(meta_csv, corpus_path):
    metadata = pd.read_csv(meta_csv, sep = "\t")[["status", "local_path"]]
    listed_paths = metadata.loc[metadata["status"] == "pri"]["local_path"].dropna().values.tolist()
    ms_count = 0
    print(len(listed_paths))
    for path in listed_paths:
        full_path = corpus_path + "/" + path.split("../")[-1]
        print(full_path)
        if os.path.exists(full_path):
            with open(full_path, encoding = "utf-8") as f:
                text = f.read()
                f.close()
            last_ms = int(re.findall(r"\sms(\d+)", text)[-1])
            print(last_ms)
            ms_count = ms_count + last_ms
    return ms_count


# path = "D:/Corpus Stats/2021/Cluster data/Oct_2021/parquet/"

# maxi, cl_df = fetch_largest(path)

meta_csv = "D:/Corpus Stats/2021/OpenITI_metadata_2021-2-5_merged_wNoor.csv"
corpus_path = "D:/OpenITI Corpus/corpus_10_21"

ms_total = count_corpus_ms(meta_csv, corpus_path)

