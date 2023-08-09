# -*- coding: utf-8 -*-
"""
Created on Fri May 27 14:38:58 2022

@author: mathe
"""
import pandas as pd
import pyarrow.parquet as pq
import os
from tqdm import tqdm

def load_all_cls(parquet_path, meta_path, max_date = 900, cluster_cap = 500, drop_strings = False, drop_dates = True):
    os.chdir(parquet_path)
    all_cls = pd.DataFrame()
    print("Loading all clusters below: " + str(cluster_cap))
    for root, dirs, files in os.walk(".", topdown=False):
        for name in tqdm(files):
            pq_path = os.path.join(root, name)
            if not drop_strings:            
                data = pq.read_table(pq_path).to_pandas()[["cluster", "size", "seq", "series", "text", "begin", "end"]]
            else:
                data = pq.read_table(pq_path).to_pandas()[["cluster", "size", "seq", "series", "begin", "end"]]
            if cluster_cap is not None:
                data = data[data["size"] < cluster_cap]

            all_cls = pd.concat([all_cls, data])
    
    
    
    # Use metadata to filter according to requirements
    # Add book URI to make easier to read outputs
    meta_df = pd.read_csv(meta_path, sep="\t")[["id", "book", "date"]]
    all_cls["id"] = all_cls["series"].str.split("-").str[0]
    all_cls = pd.merge(all_cls, meta_df, how = "inner", on ="id")

    print("New cluster data loaded...")

    # Applying the date filter to output
    all_cls = all_cls[(all_cls["date"] <= max_date)]
    if drop_dates:
        all_cls = all_cls.drop(columns = ["date"])
    
    return all_cls

