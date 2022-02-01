# -*- coding: utf-8 -*-
"""
Created on Wed Jun 16 15:46:31 2021

@author: mathe
"""

import matplotlib.pyplot as plt
from matplotlib import ticker
import pandas as pd

def plot_dynasty_map(csv_section, out, text_title, columns = [{"data": "fatimid", "label": "Fatimid"}, {"data": "ayyubid", "label": "Ayyubid"}, {"data": "mamluk", "label": "Mamluk"}], other_cat = None, csv_ms = None, multiples = True, thres = 1):
    
    df_section = pd.read_csv(csv_section)
    
    if csv_ms is not None:    
        data = pd.read_csv(csv_ms)
    else:
        data = df_section.copy()
    
    
    
    
    fig, axs = plt.subplots(len(columns), 1, sharex = True, sharey = True)
    fig.set_size_inches(20, 10)
    
    col_list = []
    for column in columns:
        col_list.append(column["data"])
    
    ch_col_list = col_list[:]
    if multiples:
        if "first-century" in ch_col_list:
            ch_col_list.remove("first-century")
        col_no = len(ch_col_list)
        zerow = []
        for i in range(0, col_no):
            zerow.append(0)
        print(zerow)
        multiples_list = []
        list_in = data.values.tolist()
        inv_col_no = 0 - col_no
        for row in list_in:
            if row[inv_col_no:] == zerow:
                continue
            else:
                count = 0
                for item in row[inv_col_no:]:
                    if item >= 1:
                        count = count + 1
                    if count > thres:
                        
                        multiples_list.append(row)
                        break
        
        print("Number of sections:" + str(len(list_in)))
        print("Number of multiples:" + str(len(multiples_list)))
        data_multiple = pd.DataFrame(multiples_list, columns = data.columns)
        
        
                               
    
    max_val = data[col_list].values.max(1).max()
    
    for idx, column in enumerate(columns):
        axs[idx].plot("mid_pos", column["data"], linestyle = '-', data = data, label=column["label"], alpha = 0.8, linewidth = 0.7, color = column["colour"])
        axs[idx].set_ylabel(column["label"])
        axs[idx].xaxis.set_major_formatter(ticker.StrMethodFormatter("{x:.0f}"))
        if multiples:
            axs[idx].vlines("st_pos", ymin = 0 - (max_val/5), ymax = 0 - (max_val/100), colors= 'black', data=df_section, linewidth = 0.2, label = "Section\nboundary", alpha = 0.4)
        axs[idx].vlines("st_pos", ymin = 0 - (max_val/5), ymax = 0 - (max_val/100), colors= 'red', data=data_multiple, linewidth = 0.2, label = "Multiple dates")
    
    
    # data_list = data[["st_pos", "Topic_id"]].values.tolist()
    # for row in data_list:
    #     if row[1] != 0:
    #         plt.vlines(row[0], 0, 10, label = "Topic: " + str(row[1]), linewidth = 0.7, linestyle = ':', color = 'red')
            
    
    
    plt.xlabel("Number of words into the " + text_title)
    
    
    
    plt.savefig(out, dpi=300, bbox_inches = "tight")
    
    plt.show
    return data_multiple


df = "C:/Users/mathe/Documents/Github-repos/fitna-study/dates_analysis/mappings/ms/0733Nuwayri.NihayaArab.Shamela0010283-ara1.completed.dates_tagged.ms_mapped.csv"
df_ms = "C:/Users/mathe/Documents/Github-repos/fitna-study/dates_analysis/mappings/ms/0845Maqrizi.Mawaciz.Shamela0011566-ara1.completed.dates_tagged.ms_mapped.csv"

dyn_columns = [{"data": "first-century", "label": "First century", "colour" : "purple"},
                {"data": "pre-fatimid", "label": "Pre-Fatimid", "colour" : "orange"},
               {"data": "fatimid", "label": "Fatimid", "colour": "green"}, 
               {"data": "ayyubid", "label": "Ayyubid", "colour": "red"}, 
               {"data": "mamluk", "label": "Mamluk", "colour": "blue"}]

df = plot_dynasty_map(df, "nuw_sec_sub_ppt.png", "Niḥāya", columns = dyn_columns)


