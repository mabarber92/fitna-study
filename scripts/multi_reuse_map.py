# -*- coding: utf-8 -*-
"""
Created on Thu Aug 18 10:48:42 2022

@author: mathe
"""

"""Add ability to get section offsets within the function - to improve overall
accuracy of offset matches"""


import re
import pandas as pd
from pattern_mapping_cat import pattern_map_cat

def multi_reuse_map(all_cls, tagged_text_path, dir_out, reused_texts = [], section_map = False, tops = None, date_cats = []):
    """For reused texts supply just 0000author.book URIs - the selection of all_cls will
    determine which version is used"""
    # Get filename
    text_name = tagged_text_path.split("/")[-1]
    
    # Get cluster locs from the text
    with open(tagged_text_path, encoding = "utf-8-sig") as f:
        tagged_text = f.read()
        f.close()
    
    print("getting cluster locs")
    cluster_locs = re.finditer(r"@cl([be])@?\d*@(\d+)@", tagged_text)
    cluster_offsets = {}
    for cluster in cluster_locs:
        cluster_no = cluster.group(2)
        if cluster_no not in cluster_offsets.keys():
            cluster_offsets[cluster_no] = {}
        if cluster.group(1)== "b":
            cluster_offsets[cluster_no]["ch_start_tar"] = cluster.start()
        if cluster.group(1) == "e":
            cluster_offsets[cluster_no]["ch_end_tar"] = cluster.start()
    
    print("cluster offsets calculated")
    print(cluster_offsets)
    # Fetch clusters and create compressed data for selected reused texts
    filtered_clusters = pd.DataFrame()
    if reused_texts == []:
        print("Excluding main text:" + ".".join(text_name.split(".")[0:2]))
        filtered_clusters = all_cls[all_cls["book"] != ".".join(text_name.split(".")[0:2])]
    else:
        for reused_text in reused_texts:
            print(reused_text)
            book_data = all_cls[all_cls["book"] == reused_text]
            print(book_data)
            filtered_clusters = pd.concat([filtered_clusters, book_data])
        
    print(filtered_clusters)
    # Loop through clusters and create the df
    reuse_map_out = []
    for cluster in cluster_offsets.keys():
        
        cluster_data = filtered_clusters[filtered_clusters["cluster"] == int(cluster)][["book", "seq"]].values.tolist()
        cluster_start = cluster_offsets[cluster]["ch_start_tar"]
        cluster_end = cluster_offsets[cluster]["ch_end_tar"]
        print(cluster_data)
        for book in cluster_data:
            
            reuse_map_out.append({"Text": book[0], "ch_start_tar":cluster_start, "ch_end_tar":cluster_end, "source_book_ms": book[1]})
    
    reuse_out = pd.DataFrame(reuse_map_out)
    
    reuse_out_path = dir_out + "/" + text_name + "-reuse.csv"        
    reuse_out.to_csv(reuse_out_path)    
        
    if section_map:
        print("Creating section map")
        # Add code here for section map - output to the same directory
        section_df = pattern_map_cat(tagged_text, char_counts = True, tops = tops, date_cats = date_cats)
        section_out_path = dir_out + "/" + text_name + "-section.csv"   
        section_df.to_csv(section_out_path)
        


text_in = "C:/Users/mathe/Documents/Github-repos/fitna-study/text_reuse/clusters_tagged/0845Maqrizi.Mawaciz.sectionKhirabFustat.cl-tagged"
reused_texts = ["0845Maqrizi.ItticazHunafa",
"0845Maqrizi.Mawaciz",
"0845Maqrizi.Muqaffa",
"0845Maqrizi.Rasail",
"0845Maqrizi.ShudhurCuqud",
"0845Maqrizi.Suluk"
]
out_dir = "C:/Users/mathe/Documents/Github-repos/fitna-study/text_reuse/maps"
