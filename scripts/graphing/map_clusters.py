# -*- coding: utf-8 -*-
"""
Created on Fri Oct 22 09:52:52 2021

@author: mathe
"""

import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib import patches
import pandas as pd
import json
import numpy as np

def plot_clusters(csv_section, clusters_json, out, text_title):
    
    fig, axs = plt.subplots(1, 1)
    fig.set_size_inches(10, 15)
    
    df_section = pd.read_csv(csv_section)
    with open(clusters_json) as f:
        data = f.read()
        f.close

    dict_list = json.loads(data)
    
    max_val = len(dict_list)
    spacing = 100/max_val
    
    color_mapping_1 = cm.get_cmap("tab20") # 20 cols
    color_mapping_2 = cm.get_cmap("Set3") # 12 Cols
    color_mapping_3 = cm.get_cmap("Pastel1") # 9 Cols
    
    axs.vlines("st_pos", ymin = -1, ymax = -0.1, colors= 'black', data=df_section, linewidth = 0.2, label = "Section\nboundary", alpha = 0.8)
    
    # bottom = 1
    
    
    for item in dict_list:
        clus_id = item["cluster"]
        if clus_id < 20:
            color = color_mapping_1(clus_id)
        elif clus_id < 32:
            color = color_mapping_2(clus_id-20)
        elif clus_id < 41:
            color = color_mapping_3(clus_id-32)
        else:
            print("Cluster id " + clus_id + " exceeds colour map length!")
            color = "grey"
        
        for section in item["sections"]:
            sec_width = (section["mid_pos"] - section["st_pos"])*2
            patch = patches.Rectangle(xy = (section["st_pos"], clus_id), width = sec_width, height = 0.8, color = color)
            axs.add_patch(patch)
            # plt.vlines(section["st_pos"], ymin = bottom, ymax = top, colors= color, linewidth = width, label = clus_id, alpha = 1)
        # bottom = bottom + 1
        
    
            
    plt.yticks(np.arange(1, max_val + 1, 1.0))
    

    
    
    plt.xlabel("Number of words into the " + text_title)
    
    
    
    plt.savefig(out, dpi=300, bbox_inches = "tight")
    
    plt.show
    

json_path = "C:/Users/mathe/Documents/Github-repos/fitna-study/dates_analysis/khit_date_clusters_non_dup/new_data/louvain_weighted_clusters_threshold1_cluster_count_11.json"
sections = "C:/Users/mathe/Documents/Github-repos/fitna-study/dates_analysis/mappings_updated/sections/0845Maqrizi.Mawaciz.MAB02082022-ara1.completed.dates_tagged.s_mapped.csv"

plot_clusters(sections, json_path, "Khit_test_cl1_lovain_weighted_revised.png", "Khitat -  Threshold 1 - No duplicates")

