# Ammendments : categorise each section by pre-Fatimid, Ayyubid or Mamluk - 
# Have it search for tagged dates not set format of section headers in muq

import re
import pandas as pd
import os



def count_dates_seq(text, on = "head", tops = False, w_counts = False):
    if on == "head":
        split_seps = re.split(r"(###\s\|\|\|\s)", text)
        splits = []
        for split_sep in split_seps:
            if split_sep != "### ||| ":
                splits.append("### ||| " + split_sep)
    if on == "ms":
        splits = re.split(r"ms\d+", text)
    
    out = []
    columns = ["section"]
    if w_counts:
        columns.append("st_pos")
        columns.append("mid_pos")
        columns.append("w_count")
    
    
    columns.append("date")
    columns.append("century")
    columns.append("25-y")
    columns.append("Name")
    
    if tops:
        columns.append("Topic_id")
    
    word_counter = 0
 
    
    
    for idx, split in enumerate(splits):
        print('.', end = '')
        temp = [idx + 1]
        
        if w_counts:
            temp.append(word_counter)
            sec_length = len(re.split(r"\s", split))
            temp.append(word_counter + (sec_length/2))
            word_counter = word_counter + sec_length
            temp.append(sec_length)
            
            
        d_dates = re.findall("###\s\|\|\|.*-\s.*\[-?.*(\d\d\d)\]", split)
        print(d_dates)
        if len(d_dates) >= 1:
            d_date = d_dates[0]
            century = int(d_date[0] + "00")
            if len(d_date) == 2:
                d_date = "0" + d_date
            print(d_date[1:3])
            
            if int(d_date[1:3]) <= 25:
                y25 = century + 25
                print("25")
            elif int(d_date[1:3]) <= 50:
                y25 = century + 50
                print("50")
            elif int(d_date[1:3]) <= 75:
                y25 = century + 75
                print("75")
            else:
                y25 = century
                print("100")
            name = re.findall("###\s\|\|\|.*-\s(.*)\[.*\]", split)[0]
            
            temp.extend([int(d_date), century, y25, name])
        else:
            continue
        
            
        if tops:            
            topic = re.findall(r"@TPC@(\d+)@", split)
            if len(topic) >= 1:
                temp.append(int(topic[0]))
            else:
                temp.append(0)
        print(temp)
        out.append(temp)
    
    out_df = pd.DataFrame(out, columns = columns)
    
    return out_df

path_parent = os.path.dirname(os.getcwd())

path = path_parent + "/whole text tagger/inputs/0845Maqrizi.Muqaffa.Shamela19Y0145334-ara1"

with open(path, encoding = "utf-8") as f:
    text = f.read()
    f.close()


out = count_dates_muq(text, w_counts = True)

out.to_csv("muq_bio_dates.csv", index = False)