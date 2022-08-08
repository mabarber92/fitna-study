# -*- coding: utf-8 -*-
"""
Created on Mon Aug  8 16:37:41 2022

@author: mathe
"""

from load_all_cls import load_all_cls
import pandas as pd

def text_reuse_earliest_dates_map(clusters_df, URI, ms_locs, csv_out, dyn_map = None):
    """From cluster data - finds the text according to URI - and gets earliest-dated source for each cluster, mapped to a range"""
    ms_loc_df = pd.read_csv(ms_locs)
    clusters_df = clusters_df[["cluster","begin", "end", "date", "book", "seq"]]
    cluster_list = clusters_df[clusters_df["book"] == URI][["cluster","begin", "end", "date", "book", "seq"]].values.tolist()
    
    
    data_out = []
    for cluster in cluster_list:
        cl_df = clusters_df[clusters_df["cluster"] == cluster[0]]
        earliest = cl_df[cl_df["date"] == cl_df["date"].min()].values.tolist()[0]
        if earliest[4] == URI:
            continue
        
        
        ms_pos = ms_loc_df[ms_loc_df["section"] == cluster[5]]["st_pos"].to_list()
        
        begin = ms_pos[0] + cluster[1]
        end = ms_pos[0] + cluster[2]
        
        row_out = {"cluster": cluster[0], "begin":begin, "end":end, "date":earliest[3], "book":earliest[4]}
        if dyn_map is not None:
            date = earliest[3]
            for mapping in dyn_map:
                if date >= mapping["beg"] and date < mapping["end"]:
                    row_out["label"] = mapping["label"]
                    row_out["colour"] = mapping["colour"]
        data_out.append(row_out)
    
    out_df = pd.DataFrame(data_out)
    out_df.to_csv(csv_out)


parquet_path = "D:/Corpus Stats/2021/Cluster data/Oct_2021/parquet"
meta_path = "D:/Corpus Stats/2021/OpenITI_metadata_2021-2-5_merged_wNoor.csv"
URI = "0845Maqrizi.Mawaciz"
csv_out = "C:/Users/mathe/Documents/Github-repos/fitna-study/dates_analysis/mappings_updated_chars/Mawaciz_earliest_reuse_map.csv"
ms_char_locs = "C:/Users/mathe/Documents/Github-repos/fitna-study/dates_analysis/mappings_updated_chars/ms/0845Maqrizi.Mawaciz.MAB02082022-ara1.completed.dates_tagged.ms_mapped.csv"

cats = [{'beg': 1, 'end': 100, 'label': 'first-century', "colour" : "saddlebrown"}, 
        {'beg': 101, 'end': 357, 'label': 'pre-fatimid', "colour" : "orange"}, 
        {'beg': 358, 'end': 567, 'label': 'fatimid', "colour": "green"},
        {'beg': 568, 'end': 648, 'label': 'ayyubid', "colour": "red"},
        {'beg': 649, 'end': 900, 'label': 'mamluk', "colour": "blue"}]

# all_cls = load_all_cls(parquet_path, meta_path, max_date = 846, drop_strings = True, drop_dates = False)
# text_reuse_earliest_dates_map(all_cls, URI, ms_char_locs, csv_out, dyn_map = cats)
    