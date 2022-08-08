# -*- coding: utf-8 -*-
"""
Created on Mon Aug  8 13:35:54 2022

@author: mathe
"""

import matplotlib.pyplot as plt
from matplotlib import ticker
import pandas as pd

def plot_dynasty_date_scatter(csv_dates, csv_section, out, text_title, columns = [{"data": "fatimid", "label": "Fatimid"}, {"data": "ayyubid", "label": "Ayyubid"}, {"data": "mamluk", "label": "Mamluk"}], other_cat = None, multiples = True, thres = 1):
    
    df_section = pd.read_csv(csv_section)[30:40]

    dates_data = pd.read_csv(csv_dates)[90:120]
    dates_data = dates_data[dates_data["date"] != 0]
    
    
    
    fig, axs = plt.subplots(1, 1, sharex = True, sharey = True)
    fig.set_size_inches(8.5, 11)
    
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
        list_in = df_section.values.tolist()
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
                    #ELSE THEN - IF COUNT == 1 - THIS IS ONLY 1 DYN ID'D - GET THE ID'D DYN - THIS WOULD BE EASIER IF PASSING IN AS DICTS
        
        
        #From column list - subset the df for the column and get the unique dyns - output to do
        unique_dyn_sects = pd.DataFrame()
        for col in columns:
            unique_dyn = df_section[df_section[col["data"]] > 0]
            
            for col_data in columns:
                if col_data["data"] == col["data"]:
                    continue
                else:
                    
                    unique_dyn = unique_dyn[unique_dyn[col_data["data"]] == 0]
                
            unique_dyn["colour"] = col["colour"]
            unique_dyn_sects = pd.concat([unique_dyn_sects, unique_dyn])
            
            #Add a total column to mappings - take the total to map the sections in these cases.
        
        
        
        print("Number of sections:" + str(len(list_in)))
        print("Number of multiples:" + str(len(multiples_list)))
        data_multiple = pd.DataFrame(multiples_list, columns = df_section.columns)
        
        
                               
    
    max_val = dates_data["date"].values.max()
    
    colour_set = dates_data["colour"].drop_duplicates().tolist()
    for colour in colour_set:
        data_subset = dates_data[dates_data["colour"] == colour]
        print(colour)
        axs.scatter("pos", "date", s=2, data = data_subset, label="label", alpha = 0.8, c = "colour")
        
    axs.xaxis.set_major_formatter(ticker.StrMethodFormatter("{x:.0f}"))
       
    axs.vlines("st_pos", ymin = 0 - (max_val/5)*1.5, ymax = 0 - (max_val/5), colors= 'black', data=df_section, linewidth = 0.2, label = "Section\nboundary", alpha = 0.4)
    axs.vlines("st_pos", ymin = 0 - (max_val/5)/2, ymax = 0 - (max_val/100), colors= 'fuchsia', data=data_multiple, linewidth = 0.2, label = "Multiple dates")
    axs.vlines("st_pos", ymin = 0 - (max_val/5), ymax = 0 - (max_val/5)/2, colors= unique_dyn_sects["colour"] , data=unique_dyn_sects, linewidth = 0.2, label = "Section\nboundary")
    
    
    # data_list = data[["st_pos", "Topic_id"]].values.tolist()
    # for row in data_list:
    #     if row[1] != 0:
    #         plt.vlines(row[0], 0, 10, label = "Topic: " + str(row[1]), linewidth = 0.7, linestyle = ':', color = 'red')
            
    
    
    plt.xlabel("Number of characters into the " + text_title)
    
    
    
    plt.savefig(out, dpi=300, bbox_inches = "tight")
    
    plt.show
    return data_multiple

dyn_columns = [{"data": "first-century", "label": "First century", "colour" : "saddlebrown"},
                {"data": "pre-fatimid", "label": "Pre-Fatimid", "colour" : "orange"},
               {"data": "fatimid", "label": "Fatimid", "colour": "green"}, 
               {"data": "ayyubid", "label": "Ayyubid", "colour": "red"}, 
               {"data": "mamluk", "label": "Mamluk", "colour": "blue"}]

csv_dates = "C:/Users/mathe/Documents/Github-repos/fitna-study/dates_analysis/mappings_updated_chars/0845Maqrizi.Mawaciz.MAB02082022-ara1.completed.dates_tagged.yy_mapped.csv"
csv_section = "C:/Users/mathe/Documents/Github-repos/fitna-study/dates_analysis/mappings_updated_chars/sections/0845Maqrizi.Mawaciz.MAB02082022-ara1.completed.dates_tagged.s_mapped.csv"

data_multiple = plot_dynasty_date_scatter(csv_dates, csv_section, "Test_scatter_subset.png", "Khiṭaṭ", columns = dyn_columns)
