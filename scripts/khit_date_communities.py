# -*- coding: utf-8 -*-
"""
Created on Tue Oct 19 15:47:12 2021

@author: mathe
"""

import networkx as nx
from cdlib import algorithms
from tqdm import tqdm
import json
import pandas as pd

def comm_detect(dict_list, node_thres = 1, cluster_thres = 1):
    g = nx.Graph()
    print("Node threshold: " + str(node_thres))
    for idx, item in enumerate(tqdm(dict_list)):
        node_list = []
        # g.add_node(item["seq"])
        for comp in dict_list[idx+1:]:
            w = 0
            if item["dates"] == "None":
                
                continue
            for date in item["dates"]:
                if date == "000":
                    
                    continue
                if date in comp["dates"]:                    
                    w = w + 1
            if w >= node_thres:
                g.add_edge(item["seq"], comp["seq"], weight = w)
                node_list.extend([item["seq"], comp["seq"]])
    unique = list(set(node_list))
    for node in unique:
        g.add_node(node)
    
    print("\ngetting communities")
    comms = algorithms.greedy_modularity(g, weight = "weight")
    comms_list = comms.communities
    print("Number of communities: " + str(len(comms_list)))
    
    print("analysing communities")
    comm_details = []
    cluster_summary = []
    for idx, comm in enumerate(tqdm(comms_list)):
        length = len(comm)
        cluster_summary.append([idx, length])
        if length > cluster_thres:
            dict_item = {"cluster": idx, "length" : length}
            cluster = []
            date_summary = {}
            for sect in dict_list:
                if sect["seq"] in comm:
                    cut_dict = {}
                    cut_dict["seq"] = sect["seq"]
                    cut_dict["title"] = sect["title"]
                    cut_dict["st_pos"] = sect["st_pos"]
                    cut_dict["mid_pos"] = sect["mid_pos"]
                    cut_dict["dates"] = sect["dates"]
                    cluster.append(cut_dict)
                    for date in sect["dates"]:
                        if date == "000":
                            continue
                        if date in date_summary.keys():
                            date_summary[date].append(sect["seq"])
                        else:
                            date_summary[date] = [sect["seq"]]
            dict_item["sections"] = cluster
            dict_item["date_list"] = date_summary
            dict_item["total_unique_dates"] = len(date_summary)
            comm_details.append(dict_item)
        
    
    return comms, comm_details, cluster_summary, len(comms_list)
            

path = "C:/Users/mathe/Documents/Github-repos/fitna-study/dates_analysis/qal_date_clusters/dated_splits_2_3_grams.json"

with open(path) as f:
    data = f.read()
    f.close

dict_list = json.loads(data)

for i in range(1, 5):
    out, details, summary, count = comm_detect(dict_list, node_thres = i)
    json_out = json.dumps(details, indent = 1)
    summary_df = pd.DataFrame(summary, columns = ['cluster_id', 'cluster_length'])
    path_out = "C:/Users/mathe/Documents/Github-repos/fitna-study/dates_analysis/qal_date_clusters/clusters_threshold" + str(i) + "_cluster_count_" + str(count) + ".json"
    csv_out = "C:/Users/mathe/Documents/Github-repos/fitna-study/dates_analysis/qal_date_clusters/summary_threshold" + str(i) + "_cluster_count_" + str(count) + ".csv"
    with open(path_out, "w", encoding = "utf-8") as f:
        f.write(json_out)
        f.close()
    summary_df.to_csv(csv_out, index = False)
    
    