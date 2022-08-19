# -*- coding: utf-8 -*-
"""
Created on Thu Aug 18 17:27:02 2022

@author: mathe
"""

import matplotlib.pyplot as plt

from matplotlib import patches
import pandas as pd

def plot_reuse(reuse_map, out, maintext, section_map = None, top_colours = None, annotation = None):
    
    reuse_df = pd.read_csv(reuse_map)

    fig, axs = plt.subplots(1, 1)
    fig.set_size_inches(10, 5)
    
    if section_map is not None:
        section_df = pd.read_csv(section_map)
        if top_colours is not None:
            for top in top_colours:
                top_sections = section_df[section_df["Topic_id"] == top["id"]]
                axs.vlines("st_pos", ymin = -1, ymax = -0.1, colors= top["colour"], data=top_sections, linewidth = 1, label = top["label"])
            axs.legend(loc='upper center', bbox_to_anchor=(1.1, 1.05), title = "Dynastic period described in section")
        else:            
            axs.vlines("st_pos", ymin = -1, ymax = -0.1, colors= 'black', data=section_df, linewidth = 1, label = "Section\nboundary")
        
        y_value_list = [-0.5]
        
    else:
        y_value_list = []
    
    text_list = reuse_df["Text"].sort_values().drop_duplicates().to_list()
    
      
    for idx, text in enumerate(text_list):
        data_dict = reuse_df[reuse_df["Text"] == text].to_dict("records")
        y_value_list.append(idx + 0.5)
        for reuse_instance in data_dict:
            sec_width = (reuse_instance["ch_end_tar"] - reuse_instance["ch_start_tar"])
            patch = patches.Rectangle(xy = (reuse_instance["ch_start_tar"], idx), width = sec_width, height = 0.9, color = "darkgrey")
            axs.add_patch(patch)
    
    if section_map is not None:
        label_list = ["Section Boundary"] + text_list
    else:
        label_list = text_list.copy
    
    if annotation is not None:
        for annot in annotation:
            plt.annotate(annot["text"], (annot["x"], annot["y"]))
    
    plt.yticks(y_value_list, label_list)
    plt.xlabel("Number of characters into the " + maintext)
    
    plt.savefig(out, dpi=300, bbox_inches = "tight")
    
    plt.show
    

out = "Igatha_self_reuse.png"
reuse_map = "C:/Users/mathe/Documents/Github-repos/fitna-study/text_reuse/maps/0845Maqrizi.IghathaUmma.Kraken210223142017.cl-tagged-reuse.csv"
section_map = "C:/Users/mathe/Documents/Github-repos/fitna-study/text_reuse/maps/0845Maqrizi.IghathaUmma.Kraken210223142017.cl-tagged-section.csv"
topics = [{"id": "@PREIS@", "colour": "brown", "label" : "Pre-Islamic"},
          {"id": "@EARIS@", "colour": "yellow", "label" : "Early Islamic"},
          {"id": "@IKH@", "colour": "orange", "label" : "Ikhshidid"},
          {"id": "@FAT@", "colour": "green", "label" : "Fatimid"},
          {"id": "@AYY@", "colour": "red", "label" : "Ayyubid"},
          {"id": "@MAM@", "colour": "darkblue", "label" : "Mamluk"},
          {"id": "None", "colour": "black", "label" : "No Dynasty"}
          ]

annotations = [{"text": "Fatimid Fitna", "x": 500, "y": -0.6},
               {"text": "Burning of Miṣr", "x": 12000, "y": -0.6},
               {"text": "Other\ncrises", "x": 17300, "y": -0.75}]


plot_reuse(reuse_map, out, "Ighāthat al-Umma", section_map = section_map, top_colours = topics)