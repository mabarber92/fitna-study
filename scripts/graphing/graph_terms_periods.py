# -*- coding: utf-8 -*-
"""
Created on Fri Aug 19 13:25:41 2022

@author: mathe
"""

import pandas as pd
import re
import matplotlib.pyplot as plt
from matplotlib import ticker

def graph_terms_periods(section_terms_csv, terms, out, text_title, focussed_dates = None, columns = [{"data": "fatimid", "label": "Fatimid"}, {"data": "ayyubid", "label": "Ayyubid"}, {"data": "mamluk", "label": "Mamluk"}], other_cat = None, csv_ms = None, reuse_map = None, multiples = True, thres = 1
                     , separate_sections_graph = False):
    
    df_section = pd.read_csv(section_terms_csv)
    terms_df = pd.read_csv(terms)
    if focussed_dates is not None:
        focussed_dates_df = pd.read_csv(focussed_dates)
    
    if csv_ms is not None:    
        data = pd.read_csv(csv_ms)
    else:
        data = df_section.copy()
    
    ### Create category aggregations and separate dfs and create category list
    term_categories = []
    for term in terms_df["Cat"].drop_duplicates().to_list():
        print(term)
        if focussed_dates is not None:
            date_range = focussed_dates_df[focussed_dates_df["Cat"] == term]
            if len(date_range) == 1:                
                date_range = date_range.values.tolist()[0]
                print(date_range)
                terms_list = []
                for i in range(int(date_range[0]), int(date_range[1])):
                    col_title = "@YY" + str(i)
                    if col_title in data.columns:
                        terms_list.append(col_title)
                cols = terms_df[terms_df["Cat"] == term]["Term"].to_list()
                cols.extend(terms_list)
            else:
                cols = terms_df[terms_df["Cat"] == term]["Term"].to_list()
        else:
            cols = terms_df[terms_df["Cat"] == term]["Term"].to_list()
        term_categories.append({"term": term, "cols": cols})

    
    print(term_categories)
    
    
    if not separate_sections_graph:
        fig, axs = plt.subplots(len(term_categories), 1, sharex = True, sharey = False)
        
    if separate_sections_graph:
        fig, axs = plt.subplots(len(term_categories) + 1, 1, sharex = True, sharey = False)
    
    fig.set_size_inches(8.5, 11)
    
    # Create aggregated data for term cats
    for cat in term_categories:
        data[cat["term"]] = data[cat["cols"]].sum(axis=1)
    
    print(data)
    
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
                    #ELSE THEN - IF COUNT == 1 - THIS IS ONLY 1 DYN ID'D - GET THE ID'D DYN - THIS WOULD BE EASIER IF PASSING IN AS DICTS
        
        
        #From column list - subset the df for the column and get the unique dyns - output to do
        unique_dyn_sects = pd.DataFrame()
        for col in columns:
            unique_dyn = data[data[col["data"]] > 0]
            
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
        data_multiple = pd.DataFrame(multiples_list, columns = data.columns)
        
        
                               
    
    max_val = data[col_list].values.max(1).max()
    
    if not separate_sections_graph:
        for idx, column in enumerate(term_categories):
            axs[idx].plot("mid_pos", column["term"], linestyle = '-', data = data, alpha = 0.8, linewidth = 0.7)
            axs[idx].set_ylabel(column["term"])
            axs[idx].xaxis.set_major_formatter(ticker.StrMethodFormatter("{x:.0f}"))
            max_val = data[column["term"]].values.max()
            axs[idx].vlines("st_pos", ymin = 0 - (max_val/5), ymax = 0 - (max_val/100), colors= 'black', data=df_section, linewidth = 0.2, label = "Section\nboundary", alpha = 0.4)
            axs[idx].vlines("st_pos", ymin = 0 - (max_val/5)/2, ymax = 0 - (max_val/100), colors= 'fuchsia', data=data_multiple, linewidth = 0.2, label = "Multiple dates")
            axs[idx].vlines("st_pos", ymin = 0 - (max_val/5), ymax = 0 - (max_val/100) - (max_val/5)/2, colors= unique_dyn_sects["colour"] , data=unique_dyn_sects, linewidth = 0.2, label = "Section\nboundary")
    
    if separate_sections_graph:
        for idx, column in enumerate(term_categories):
            axs[idx].plot("mid_pos", column["term"], linestyle = '-', data = data, alpha = 0.8, linewidth = 0.7)
            axs[idx].set_ylabel(column["term"])
            axs[idx].xaxis.set_major_formatter(ticker.StrMethodFormatter("{x:.0f}"))
        if reuse_map is not None:
            reuse_df = pd.read_csv(reuse_map)
            colours_list = reuse_df["colour"].drop_duplicates().to_list()
            for colour in colours_list:
                colour_subset = reuse_df[reuse_df["colour"] == colour]
                print(colour_subset)
                axs[-1].vlines("begin", ymin = (max_val/4)*3, ymax = max_val, colors= 'colour', data=colour_subset, linewidth = 0.2, label = "Reuse", alpha = 0.4)
            
            axs[-1].vlines("st_pos", ymin = 0, ymax = (max_val/4), colors= 'black', data=df_section, linewidth = 0.2, label = "Section\nboundary", alpha = 0.4)
            axs[-1].vlines("st_pos", ymin = (max_val/4), ymax = (max_val/4)*2, colors= 'fuchsia', data=data_multiple, linewidth = 0.2, label = "Multiple dates")
            axs[-1].vlines("st_pos", ymin = (max_val/4)*2, ymax = (max_val/4)*3, colors= unique_dyn_sects["colour"] , data=unique_dyn_sects, linewidth = 0.2, label = "Section\nboundary")
                
        else:    
            axs[-1].vlines("st_pos", ymin = 0, ymax = (max_val/3), colors= 'black', data=df_section, linewidth = 0.2, label = "Section\nboundary", alpha = 0.4)
            axs[-1].vlines("st_pos", ymin = (max_val/3), ymax = (max_val/3)*2, colors= 'fuchsia', data=data_multiple, linewidth = 0.2, label = "Multiple dates")
            axs[-1].vlines("st_pos", ymin = (max_val/3)*2, ymax = max_val, colors= unique_dyn_sects["colour"] , data=unique_dyn_sects, linewidth = 0.2, label = "Section\nboundary")
            
    # data_list = data[["st_pos", "Topic_id"]].values.tolist()
    # for row in data_list:
    #     if row[1] != 0:
    #         plt.vlines(row[0], 0, 10, label = "Topic: " + str(row[1]), linewidth = 0.7, linestyle = ':', color = 'red')
            
    
    
    plt.xlabel("Number of words into the " + text_title)
    
    
    
    plt.savefig(out, dpi=300, bbox_inches = "tight")
    
    plt.show
    


dyn_columns = [{"data": "first-century", "label": "First century", "colour" : "saddlebrown"},
                {"data": "pre-fatimid", "label": "Pre-Fatimid", "colour" : "orange"},
               {"data": "fatimid", "label": "Fatimid", "colour": "green"}, 
               {"data": "ayyubid", "label": "Ayyubid", "colour": "red"}, 
               {"data": "bahri-mamluk", "label": "Bahri Mamluk", "colour": "slateblue"},
               {"data": "circassian-mamluk", "label": "Circassian Mamluk", "colour": "darkblue"}]

out = "test_terms.png"
terms_csv = "C:/Users/mathe/Documents/Github-repos/fitna-study/terms_analysis/0845Maqrizi.Mawaciz.MAB02082022-sectionterms.csv"
terms = "C:/Users/mathe/Documents/Github-repos/fitna-study/terms_analysis/terms_resources/terms_list.csv"
dates = "C:/Users/mathe/Documents/Github-repos/fitna-study/terms_analysis/terms_resources/dates_list.csv"

graph_terms_periods(terms_csv, terms, out, "Khiṭaṭ", focussed_dates = dates, columns = dyn_columns)