# -*- coding: utf-8 -*-
"""
Created on Wed Jun 16 13:19:53 2021

@author: mathe
"""

import re
from collections import Counter
import pandas as pd
import os
from tqdm import tqdm


def count_y_centuries(text_path, out_path, end_date = None, centuries = True, top_freq = 20, delete_000 = True):

    with open(text_path, encoding = "utf-8") as f:
        text = f.read()
        f.close()

    years = re.findall(r"@YY(\d{3})", text)

    distinct = Counter(years)

    distinct = dict(sorted(distinct.items(), key=lambda item: item[1], reverse = True))    
    
    if delete_000:
        del distinct["000"]
    
    
    if end_date is not None:
        remove_list = []
        date_list = distinct.keys()
        for date in date_list:
            if int(date) > end_date:
                remove_list.append(date)
        for remove_date in remove_list:
            del distinct[remove_date]
        
    df_all = pd.DataFrame.from_dict(distinct, orient='index', columns = ["Distinct count"])
    df_all.insert(0, "date", df_all.index)
    total_freq = df_all['Distinct count'].sum()
    df_all['percent'] = round((df_all['Distinct count'] / total_freq
                  ) * 100, 3)
    
    
    df_all = df_all.sort_values(by=["Distinct count"], ascending = False)
    df_all = df_all.reset_index(drop=True)
    df_all["rank"] = df_all.index
    
    # Get record of centuries if true
    
    if centuries:

        century_counts = []
        centuries_out = out_path + "_centuries/"
        if not os.path.exists(centuries_out):
            os.mkdir(centuries_out)
        
        for i in range(0,10):
            regex = r"@YY(" + str(i) + "\d{2})"
            date_list = re.findall(regex, text)
            if i == 0:
                while "000" in date_list:
                    date_list.remove("000")
            if end_date is not None:
                
                if i >= int(str(end_date)[0]):                    
                    date_list_copy = date_list.copy()
                    for date_copy in date_list_copy:                        
                        if int(date_copy) > end_date:                            
                            date_list.remove(date_copy)
            distinct_dates = Counter(date_list)    
            distinct_dates = dict(sorted(distinct_dates.items(), key=lambda item: item[1]))    
            df = pd.DataFrame.from_dict(distinct_dates, orient='index', columns = ["Distinct count"])
            
            df.to_csv(centuries_out + "century_" + str(i) + ".csv")
            
            if len(date_list) > 0:
                century_counts.append([str(i) + "00", len(distinct_dates), len(date_list)])
    
        df_cen = pd.DataFrame(century_counts, columns = ["Date", "Distinct count", "Absolute count"])
        df_cen.to_csv(out_path + ".centuries_distinct.csv")
    
    # If the top_freq doesn't equal zero - use this to get the top part of the df and add first century dates with the same
    
    if top_freq != 0:
        

        top = df_all.iloc[0:top_freq+1].to_dict("records")
        
        for row in top:
            date = row["date"]            
            if date[1:3] == "00":
                row["first_century_eq"] = "n/a"
                row["first_century_freq"] = "n/a"
                row["total"] = row["Distinct count"]
                row["Total percentage"] = row["percent"]
            if date[0] == "0":
                c_eq = date[1:3]
                df_subset = df_all[df_all["date"].str[1:3] == c_eq]
                df_subset = df_subset[df_subset["date"] != date][["date", "Distinct count"]].to_dict("records")                
                if len(df_subset) != 0:
                    df_subset = df_subset[0]
                    first_century_freq = df_subset["Distinct count"]
                    row["first_century_eq"] = df_subset["date"]
                    row["first_century_freq"] = first_century_freq
                    row["total"] = first_century_freq + row["Distinct count"]
                    row["Total percentage"] = round(((first_century_freq + row["Distinct count"])/total_freq)*100, 3)    
            else:
                
                first_c_eq = "0" + date[1:3]
                df_subset = df_all[df_all["date"] == first_c_eq][["date", "Distinct count"]].to_dict("records")                
                if len(df_subset) != 0:
                    df_subset = df_subset[0]
                    first_century_freq = df_subset["Distinct count"]
                    row["first_century_eq"] = df_subset["date"]
                    row["first_century_freq"] = first_century_freq
                    row["total"] = first_century_freq + row["Distinct count"]
                    row["Total percentage"] = round(((first_century_freq + row["Distinct count"])/total_freq)*100, 3)
                else:
                   row["first_century_eq"] = "n/a"
                   row["first_century_freq"] = "n/a"
                   row["total"] = row["Distinct count"]
                   row["Total percentage"] = row["percent"] 
        top.append({"date": "total", "Distinct count": total_freq, "percent":100, "first_century_eq": "n/a", 
                       "first_century_freq" : "n/a", "total": total_freq, "Total percentage": 100})
        
        top_df = pd.DataFrame(top)
        
        top_df.to_csv(out_path + ".top_" + str(top_freq) + ".csv")
        
    
    

    
    df_all.to_csv(out_path + ".all_dates_distinct.csv", index=False)
        


texts_input = "C:/Users/mathe/Documents/Github-repos/fitna-study/whole text tagger/outputs/new-1-8-23"
output_loc = "C:/Users/mathe/Documents/Github-repos/fitna-study/dates_analysis/date_freqs_update-1-8-23/"

for root, dirs, files in os.walk(texts_input, topdown=False):
    for name in tqdm(files):            
        text_path = os.path.abspath(os.path.join(root, name))    
        out_path = os.path.abspath(os.path.join(output_loc, name))
        count_y_centuries(text_path, out_path, end_date = 845)



