# -*- coding: utf-8 -*-
"""
Created on Thu Sep  8 16:50:09 2022

@author: mathe
"""

from load_all_cls import load_all_cls

def count_self_reuse_chs(all_cls, text_uri):
    author = text_uri.split(".")[0]
    text_cls = all_cls[all_cls["book"] == text_uri]["cluster"].to_list()
    full_cls = all_cls[all_cls["cluster"].isin(text_cls)]
    full_cls["author"] = full_cls["book"].str.split(".", n=1, expand = True)[0]
    full_cls["ch_len"] = full_cls["end"] - full_cls["begin"]
    non_self_clusters = full_cls[full_cls["author"] != author]["cluster"].to_list()
    non_self = full_cls[full_cls["cluster"].isin(non_self_clusters)]
    self_df = full_cls[~full_cls["cluster"].isin(non_self_clusters)]
    non_self_count = non_self[non_self["book"] == text_uri]["ch_len"].sum()
    self_count = self_df[self_df["book"] == text_uri]["ch_len"].sum()
    print(non_self_count)
    print(self_count)
    
    return non_self, self_df


# parquet_path = "D:/Corpus Stats/2021/Cluster data/Oct_2021/parquet"
# meta = "D:/Corpus Stats/2021/OpenITI_metadata_2021-2-5_merged_wNoor.csv"
# text_uri = "0845Maqrizi.Mawaciz"

# all_cls = load_all_cls(parquet_path, meta, drop_strings = True)

# non_self, self_df = count_self_reuse_chs(all_cls, text_uri)
        