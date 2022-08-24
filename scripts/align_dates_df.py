# -*- coding: utf-8 -*-
"""
Created on Wed Aug 24 09:06:17 2022

@author: mathe
"""

import pandas as pd

def align_dates(dates_csv1, dates_csv2, name1, name2, out, check_first_cen = True):
    df1 = pd.read_csv(dates_csv1)
    df2 = pd.read_csv(dates_csv2)
    
    # df2 = df2.sort_values(by=["Distinct count"], ascending = False)
    # df2 = df2.reset_index(drop=True)
    # df2["rank_" + name2] = df2.index
    
    df1['date'] = df1['date'].astype(str).str.zfill(3)
    df2['date'] = df2['date'].astype(str).str.zfill(3)
    dict_out = df1.merge(df2, how = 'inner', left_on = 'date', right_on = 'date', suffixes = ('_' + name1, '_' + name2)).to_dict('records')
    
    total_freq = df2['Distinct count'].sum()
    for row in dict_out:
        date = str(row["date"]).zfill(3)            
        if date[1:3] == "00":
            row["first_century_eq"] = "n/a"
            row["first_century_freq"] = "n/a"
            row["total"] = row["Distinct count_" + name2]
            row["Total percentage"] = row["percent_" + name2]
        if date[0] == "0":
            if check_first_cen:
                c_eq = date[1:3]
                df_subset = df2[df2["date"].str[1:3] == c_eq]
                df_subset = df_subset[df_subset["date"] != date][["date", "Distinct count"]].to_dict("records")                
                if len(df_subset) != 0:
                    df_subset = df_subset[0]
                    first_century_freq = df_subset["Distinct count"]
                    row["first_century_eq"] = df_subset["date"]
                    row["first_century_freq"] = first_century_freq
                    row["total"] = first_century_freq + row["Distinct count_" + name2]
                    row["Total percentage"] = round(((first_century_freq + row["Distinct count_" + name2])/total_freq)*100, 3)
            else:
                row["first_century_eq"] = "n/a"
                row["first_century_freq"] = "n/a"
                row["total"] = row["Distinct count_" + name2]
                row["Total percentage"] = row["percent_" + name2]
        else:
            
            first_c_eq = "0" + date[1:3]
            df_subset = df2[df2["date"] == first_c_eq][["date", "Distinct count"]].to_dict("records")                
            if len(df_subset) != 0:
                df_subset = df_subset[0]
                first_century_freq = df_subset["Distinct count"]
                row["first_century_eq"] = df_subset["date"]
                row["first_century_freq"] = first_century_freq
                row["total"] = first_century_freq + row["Distinct count_" + name2]
                row["Total percentage"] = round(((first_century_freq + row["Distinct count_" + name2])/total_freq)*100, 3)
            else:
                row["first_century_eq"] = "n/a"
                row["first_century_freq"] = "n/a"
                row["total"] = row["Distinct count_" + name2]
                row["Total percentage"] = row["percent_" + name2]
    
    df_out = pd.DataFrame(dict_out)
    df_out.to_csv(out, index = False)
    
csv1 = 'C:/Users/mathe/Documents/Github-repos/fitna-study/dates_analysis/date_freqs_update/0845Maqrizi.IghathaUmma.Kraken210223142017-ara1.dyn-tagged.dates_tagged.all_dates_distinct.csv'
csv2 = 'C:/Users/mathe/Documents/Github-repos/fitna-study/dates_analysis/date_freqs_update/0845Maqrizi.Mawaciz.MAB02082022-ara1.completed.dates_tagged.all_dates_distinct.csv'

align_dates(csv1, csv2, 'Ighatha', 'Khitat', 'C:/Users/mathe/Documents/Github-repos/fitna-study/dates_analysis/date_freqs_update/Igatha_Khitat_comp.csv', check_first_cen = False)