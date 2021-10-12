# -*- coding: utf-8 -*-
"""
Created on Wed Jun 16 10:17:05 2021

@author: mathe
"""

import pandas as pd
import re



def string_y_tag (string):
    
    # Load in the conversion csv
    dates_df = pd.read_csv("C:/Users/mathe/Documents/Kitab project/Big corpus datasets/Github/arabic_date_tagger/Full_corpus_25_10/dates df.csv", dtype=str)
    
    dates_1 = dates_df[["1s", "1_no"]].dropna().values.tolist()
    dates_10 = dates_df[["10s", "10s_no"]].dropna().values.tolist()
    dates_100 = dates_df[["100s", "100s_no"]].dropna().values.tolist()
    dates_100_sep = dates_df[["100_1","100_1_no"]].dropna().values.tolist()
    start_terms = dates_df[["year", "meaning"]].dropna().values.tolist()
    exc_100 = "مائة"
    exc_100_2 = "مئة"
    # Clean the line and get the token count (for efficiency)
    line_clean = re.sub(r"ms\d+|\]|\[|\d+|[,./؟\?!()«»،:~]|###|\|", "", string)    
    line_split = line_clean.split()
    n_tok = len(line_split)
    
    # Setting digits and other values
    d1 = "0"
    d2 = "0"
    d3 = "0"
    y_type = "@YY"
    
    pos_1 = 0
    pos_2 = 1
    pos_3 = 2
    pos_4 = 3
    pos_5 = 4
    
    if n_tok >= 3:
            
            
            for digit_1 in dates_1:
                if digit_1[0] == line_split[pos_1]:
                    d1 = digit_1[1]
                    break
            for digit_2 in dates_10:
                if digit_2[0] == line_split[pos_2] or digit_2[0] == line_split[pos_1]:
                    d2 = digit_2[1]
                    break
            for digit_3 in dates_100:
                                    
                if digit_3[0] == line_split[pos_3] or digit_3[0] == line_split[pos_2] or digit_3[0] == line_split[pos_1]:
                    d3 = digit_3[1]
                    break
                                        
            if line_split[pos_2] == exc_100 or line_split[pos_2] == exc_100_2:
                for digit_1 in dates_100_sep:
                    if digit_1[0] == line_split[pos_1]:                                            
                        d3 = digit_1[1]
                        d2 = '0'
                        d1 = '0'
                        break
                                
            # Finding cases of 'ba'd miyya'
            if line_split[pos_3] == "بعد":                                
                                                        
                try:
                    if line_split[pos_5] == exc_100 or line_split[pos_5] == exc_100_2:
                        for digit_1 in dates_100_sep:
                            if digit_1[0] == line_split[pos_4]:
                                d3 = digit_1[1]
                                break
                except IndexError:
                    pass                                                        
                try:
                    for digit_3 in dates_100:
                        if digit_3[0] == line_split[pos_4]:
                            d3 = digit_3[1]
                            break
                except IndexError:
                    pass
                                
                # Exceptions - split 100s and non-chronicle year types
                try:
                    if line_split[pos_2] == "مولده" or line_split[pos_3] == "مولده" or line_split[pos_4] == "مولده" or line_split[pos_5] == "مولده":
                        y_type = '@YF'
                except IndexError:
                    pass
            if line_split[pos_2] == "من" :
                    if line_split[pos_3] == "ولاية" or line_split[pos_3] == "سلطنة":
                        y_type = "@YR"
                    if line_split[pos_3] == "مولده" or line_split[pos_3] == "الفيل":
                        y_type = "@YF"
                                    
                    if line_split[pos_3] == "النبوة" or line_split[pos_3] == "البعثة":
                        y_type = "@YP"
                    if line_split[pos_3] == "النبوة" or line_split[pos_3] == "البعثة":
                        y_type = "@YP"
            if line_split[pos_2] == "ولاية" :
                        y_type = "@YR"
            elif line_split[pos_3] == exc_100 or line_split[pos_3] == exc_100_2:
                                   
                        for digit_1 in dates_100_sep:
                            if digit_1[0] == line_split[pos_2]:
                                d3 = digit_1[1]
            elif line_split[pos_3] == "من" :
                        try:    
                            if line_split[pos_4] == "ولاية" or line_split[pos_4] == "سلطنة":
                                y_type = "@YR"
                            if line_split[pos_4] == "مولده" or line_split[pos_4] == "الفيل":
                                y_type = "@YF"
                                        
                            if line_split[pos_4] == "النبوة" or line_split[pos_4] == "البعثة":
                                y_type = "@YP"
                        except IndexError:
                            pass
            try:
                                    
                if line_split[pos_4] == exc_100 or line_split[pos_4] == exc_100_2:
                                            
                    for digit_1 in dates_100_sep:
                        if digit_1[0] == line_split[pos_3]:
                            d3 = digit_1[1]
                    # Dropping cases where the year is regnal
                elif line_split[pos_4] == "من" :
                                if line_split[pos_5] == "ولاية" or line_split[pos_5] == "سلطنة":
                                    y_type = "@YR"
                                if line_split[pos_5] == "مولده" or line_split[pos_5] == "الفيل":
                                    y_type = "@YF"
                                    
            except IndexError:
                pass
            if line_split[pos_3] == "ولاية" :
                y_type = "@YR"
                                    
                                
                            

    elif n_tok == 2:
            for digit_1 in dates_1:
                if digit_1[0] == line_split[pos_1]:
                    d1 = digit_1[1]
                    break
            for digit_2 in dates_10:
                if digit_2[0] == line_split[pos_2] or digit_2[0] == line_split[pos_1]:
                    d2 = digit_2[1]
                    break
            for digit_3 in dates_100:
                if digit_3[0] == line_split[pos_2] or digit_3[0] == line_split[pos_1]:
                    d3 = digit_3[1]
                    break
                if line_split[pos_2] == exc_100 or line_split[pos_2] == exc_100_2:
                    for digit_1 in dates_100_sep:
                        if digit_1[0] == line_split[pos_1]:
                            d3 = digit_1[1]
                            d2 = '0'
                            d1 = '0'
                            break
                            
                            

    elif n_tok == 1:
            for digit_1 in dates_1:
                if digit_1[0] == line_split[pos_1]:
                    d1 = digit_1[1]
                    break
            for digit_2 in dates_10:
                if digit_2[0] == line_split[pos_1]:
                    d2 = digit_2[1]
                    break
            for digit_3 in dates_100:
                if digit_3[0] == line_split[pos_1]:
                    d3 = digit_3[1]
                    break
 
    
    year = y_type + d3 + d2 + d1
    return year
    
    
    


def date_sub(m):
    print('.', end = '')
    date_string = m.group(0)
    date_tag = string_y_tag(date_string)        
    return " " + date_tag + date_string
        



path = "D:/OpenITI Corpus/latest_corpus_02_21/data/0845Maqrizi/0845Maqrizi.Mawaciz/0845Maqrizi.Mawaciz.Shamela0011566-ara1.completed"
out_path = "C:/Users/mathe/Documents/Kitab project/Big corpus datasets/date_tagged_corpus/whole text tagger/outputs/0845Maqrizi.Mawaciz.Shamela0011566-ara1.date_tagged"

with open(path, encoding = "utf-8") as f:
            text = f.read()
            f.close()

sana = "سنة"
text = re.sub(r"(?<=%s)((\s?\n[#~][~\s]?)?\s?(\n#)?\w+[.,:،؟?]?){5}" % (sana), date_sub, text)

with open(out_path, "w", encoding = "utf-8") as f:
    f.write(text)
    f.close()
    