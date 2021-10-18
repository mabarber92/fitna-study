# -*- coding: utf-8 -*-
"""
Created on Wed Jun 16 15:46:31 2021

@author: mathe
"""

import matplotlib.pyplot as plt
import pandas as pd

def plot_dynasty_map(csv, out, text_title, columns = [{"data": "fatimid", "label": "Fatimid"}, {"data": "ayyubid", "label": "Ayyubid"}, {"data": "mamluk", "label": "Mamluk"}], other_cat = None):

    data = pd.read_csv(csv)
    
    fig, axs = plt.subplots(1, 1)
    fig.set_size_inches(10, 6)
    
    col_list = []
    for column in columns:
        col_list.append(column["data"])
        
    max_val = data[col_list].values.max(1).max()
    
    for column in columns:
        plt.plot("mid_pos", column["data"], linestyle = '-', data = data, label=column["label"], alpha = 0.6, linewidth = 0.7)
    
    plt.vlines("st_pos", ymin = 0 - (max_val/10), ymax = 0 - (max_val/100), colors= 'black', data=data, linewidth = 0.2, label = "Section\nboundary")
    
    # data_list = data[["st_pos", "Topic_id"]].values.tolist()
    # for row in data_list:
    #     if row[1] != 0:
    #         plt.vlines(row[0], 0, 10, label = "Topic: " + str(row[1]), linewidth = 0.7, linestyle = ':', color = 'red')
            
    
    plt.legend(title = "Term or topic\nnumber", loc = "upper right")
    plt.xlabel("Number of words into the " + text_title)
    plt.ylabel("Number of mentions of date related to dynasty")
    plt.title("Number of mentions of different dynasties in the " + text_title)
    
    plt.savefig(out, dpi=300, bbox_inches = "tight")
    
    plt.show


df = "C:/Users/mathe/Documents/Github-repos/fitna-study/dates_analysis/mappings/sections/0733Nuwayri.NihayaArab.Shamela0010283-ara1.completed.dates_tagged.s_mapped.csv"


plot_dynasty_map(df, "test_function.png", "Nihaya")


