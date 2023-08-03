# -*- coding: utf-8 -*-
"""
Created on Fri Aug 19 13:25:41 2022

@author: mathe
"""

import pandas as pd
import re
import matplotlib.pyplot as plt
from matplotlib import ticker
from matplotlib import patches
import seaborn as sns

def create_area_dict(map_df, sum_col, bin_width = 5000):
    dict_list_out = []
    # Proxy for char total while we prove viability of graphing approach
    char_total = int(map_df["mid_pos"].max())      
    for i in range(0, char_total, bin_width):
        
        filtered_data = map_df[map_df["st_pos"].between(i, i+bin_width-1)]        
        total_count = filtered_data[sum_col].sum()
        if total_count > 0:
            dict_list_out.append({"xy": (i, 0), "width":bin_width-1, "height": total_count})
    return dict_list_out

def plot_counts_as_area(axs, map_df, sum_col, bin_width = 2500):
    area_dict_list = create_area_dict(map_df, sum_col, bin_width)
    for area_dict in area_dict_list:
        patch = patches.Rectangle(xy=area_dict["xy"], width=area_dict["width"], height=area_dict["height"], color="grey")
        axs.add_patch(patch)

def plot_cumulative_count(axs, map_df, cumul_col, label, add_diagonal_line = False):
    map_df = map_df.sort_values(by=["mid_pos"])
    data_dict_list = map_df.to_dict("records")
    cumulative_data_dicts = [{"mid_pos": 0, "Cumulative Count": 0}]    
    cumulator = 0

    for data_dict in data_dict_list:
        cumulator = cumulator + data_dict[cumul_col]

        cumulative_data_dicts.append({"mid_pos": data_dict["mid_pos"], "Cumulative Count": cumulator})
    data_df = pd.DataFrame(cumulative_data_dicts)
    
    data_df.to_csv("cumulative_data_check.csv")
    axs.plot("mid_pos", "Cumulative Count", linestyle = '-', data = data_df, linewidth = 0.5, label=label, alpha=0.7)
    if add_diagonal_line:
        axs.axline([0,0], [map_df["mid_pos"].max(), map_df[cumul_col].sum()], linestyle=':', linewidth=0.5, color='grey')

    return data_df["Cumulative Count"].max()


def graph_terms_periods(section_terms_csv, out, text_title, set_col = None, terms = None, focussed_dates = None, columns = [{"data": "fatimid", "label": "Fatimid"}, {"data": "ayyubid", "label": "Ayyubid"}, {"data": "mamluk", "label": "Mamluk"}], other_cat = None, csv_ms = None, reuse_map = None, multiples = True, thres = 1
                     , separate_sections_graph = False, plot_width = 7, plot_height = 11, area_plot=True, cumulative_plot = False, y_label_term="term"):
    
    # Use a seaborn theme for the plot
    sns.set_style("whitegrid", {"grid.linestyle": ':'})

    df_section = pd.read_csv(section_terms_csv)
    
    if focussed_dates is not None:
        focussed_dates_df = pd.read_csv(focussed_dates)
    
    if csv_ms is not None:    
        data = pd.read_csv(csv_ms)
    else:
        data = df_section.copy()
    
    if set_col is not None:
        print("Using fixed column list")
        print(set_col)
        term_categories = set_col.copy()
    else:    
        terms_df = pd.read_csv(terms)
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
        
        # Create aggregated data for term cats
        for cat in term_categories:
            data[cat["term"]] = data[cat["cols"]].sum(axis=1)
    
    if not separate_sections_graph:
        if cumulative_plot:
            fig, axs = plt.subplots(1, 1, sharex = True, sharey = False)
        else:
            fig, axs = plt.subplots(len(term_categories), 1, sharex = True, sharey = False)
        
    if separate_sections_graph:
        fig, axs = plt.subplots(len(term_categories) + 1, 1, sharex = True, sharey = False)
    
    fig.set_size_inches(plot_width, plot_height)
    
    
    
    
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
        
        
                               
    
    if len(col_list) > 0:
        max_val = data[col_list].values.max(1).max()
    
    if not separate_sections_graph:
        if len(term_categories) == 1 or cumulative_plot:
            # column = term_categories[0]
            max_vals = []
            for column in term_categories:
                print(axs)
                max_val = data[column["term"]].values.max()
                if cumulative_plot:
                    max_val = plot_cumulative_count(axs, data, column["term"], column["label"])                
                elif area_plot:
                    plot_counts_as_area(axs, data, column["term"])
                else:
                    axs.plot("mid_pos", column["term"], linestyle = '-', data = data, alpha = 0.8, linewidth = 0.7)
                max_vals.append(max_val)
            if len(term_categories) == 1:
                axs.set_ylabel(column["label"])
            else:
                axs.set_ylabel("Cumulative count of {}".format(y_label_term))
                axs.legend()
            print(max_vals)
            max_val = max(max_vals)
            axs.xaxis.set_major_formatter(ticker.StrMethodFormatter("{x:.0f}"))            
            axs.vlines("st_pos", ymin = 0 - (max_val/10), ymax = 0 - (max_val/100), colors= 'black', data=df_section, linewidth = 0.2, label = "Section\nboundary", alpha = 0.4)
            if multiples:
                axs.vlines("st_pos", ymin = 0 - (max_val/10)/2, ymax = 0 - (max_val/100), colors= 'fuchsia', data=data_multiple, linewidth = 0.2, label = "Multiple dates")
                axs.vlines("st_pos", ymin = 0 - (max_val/10), ymax = 0 - (max_val/100) - (max_val/5)/2, colors= unique_dyn_sects["colour"] , data=unique_dyn_sects, linewidth = 0.2, label = "Section\nboundary")
            tick_list = []
            if not area_plot or not cumulative_plot:
                for i in range(0, max_val +1, 1):
                    tick_list.append(i)
                axs.set_yticks(tick_list)
            if cumulative_plot:
                for i in range(0, max_val +1, 5):
                    tick_list.append(i)
                print(tick_list)
                axs.set_yticks(tick_list)
        
            
        else:
            for idx, column in enumerate(term_categories):
                axs[idx].plot("mid_pos", column["term"], linestyle = '-', data = data, alpha = 0.8, linewidth = 0.7)
                axs[idx].set_ylabel(column["term"])
                axs[idx].xaxis.set_major_formatter(ticker.StrMethodFormatter("{x:.0f}"))
                max_val = data[column["term"]].values.max()
                axs[idx].vlines("st_pos", ymin = 0 - (max_val/5), ymax = 0 - (max_val/100), colors= 'black', data=df_section, linewidth = 0.2, label = "Section\nboundary", alpha = 0.4)
                if multiples:
                    axs[idx].vlines("st_pos", ymin = 0 - (max_val/5)/2, ymax = 0 - (max_val/100), colors= 'fuchsia', data=data_multiple, linewidth = 0.2, label = "Multiple dates")
                    axs[idx].vlines("st_pos", ymin = 0 - (max_val/5), ymax = 0 - (max_val/100) - (max_val/5)/2, colors= unique_dyn_sects["colour"] , data=unique_dyn_sects, linewidth = 0.2, label = "Section\nboundary")
                tick_list = []
                for i in range(0, max_val + 1, 1):
                    tick_list.append(i)
                axs[idx].set_yticks(tick_list)
                
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
            if multiples:
                axs[-1].vlines("st_pos", ymin = (max_val/4), ymax = (max_val/4)*2, colors= 'fuchsia', data=data_multiple, linewidth = 0.2, label = "Multiple dates")
                axs[-1].vlines("st_pos", ymin = (max_val/4)*2, ymax = (max_val/4)*3, colors= unique_dyn_sects["colour"] , data=unique_dyn_sects, linewidth = 0.2, label = "Section\nboundary")
                    
        else:    
            axs[-1].vlines("st_pos", ymin = 0, ymax = (max_val/3), colors= 'black', data=df_section, linewidth = 0.2, label = "Section\nboundary", alpha = 0.4)
            if multiples:
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

out = "Khitat_806_mentions_cumulative_test_comp.png"
terms_csv = "C:/Users/mathe/Documents/Github-repos/fitna-study/release-08-09-2022/dates_data/0845Maqrizi.Mawaciz.MAB02082022.sections-top10-dates.csv"
terms = "C:/Users/mathe/Documents/Github-repos/fitna-study/terms_analysis/terms_resources/terms_list.csv"
dates = "C:/Users/mathe/Documents/Github-repos/fitna-study/terms_analysis/terms_resources/dates_list.csv"
set_col = [{"term": "@YY806", "cols": ["@YY806"], "label": "Cumulative mentions of 806AH"}, 
           {"term": "@YY700", "cols": ["@YY700"], "label": "Cumulative mentions of @YY700"},
           {"term": "@YY790", "cols": ["@YY790"], "label": "Cumulative mentions of @YY700"},
           {"term": "@YY358", "cols": ["@YY358"], "label": "Cumulative mentions of @YY700"},
           {"term": "@YY516", "cols": ["@YY516"], "label": "Cumulative mentions of @YY700"},
           {"term": "@YY725", "cols": ["@YY725"], "label": "Cumulative mentions of @YY700"},
           {"term": "@YY567", "cols": ["@YY576"], "label": "Cumulative mentions of @YY700"}]

set_col = [{"term": "@YY806", "cols": ["@YY806"], "label": "806AH / 1403-4CE"}, 
           {"term": "@YY725", "cols": ["@YY700"], "label": "725AH / 1324-5CE"},                
           {"term": "@YY567", "cols": ["@YY567"], "label": "567AH / 1171-2CE"},
           {"term": "@YY358", "cols": ["@YY358"], "label": "358AH / 968-9CE"}]


graph_terms_periods(terms_csv, out, "Ḫiṭaṭ", set_col = set_col, columns = [], multiples=False, plot_height = 5, cumulative_plot=True, y_label_term="date")