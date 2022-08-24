# -*- coding: utf-8 -*-
"""
Created on Tue Aug 16 17:41:38 2022

@author: mathe
"""

import re
import pandas as pd

def extract_head_dyn_loc(text, csv_out, columns_out, code_dict, marker_re = r"###\s.*\n"):
    headers = re.finditer(marker_re, text)
    out = []
    for head in headers:
        match = head.group(0)
        title = re.sub("@.*@", "", match)
        dyn_code = re.findall(r"@.*@", match)
        if len(dyn_code) == 0:
            continue
        dyn_code = dyn_code[0]
        dyn = code_dict[dyn_code]
        loc = head.start()
        out.append({"title": title, "dyn_code": dyn_code, "dyn" : dyn, "char_loc":loc})
     
    
    out_df = pd.DataFrame(out)
    
    for col in columns_out:
        out_df[col] = False
    
    out_df.to_csv(csv_out, encoding = 'utf-8-sig')
    

code_dict ={
    "@PREIS@" : "Pre-Islamic",
    "@EARIS@": "Early Islam",
    "@IKH@" : "Ikhshidid",
    "@FAT@" : "Fatimid",
    "@AYY@" : "Ayyubid",
    "@MAM@" : "Mamluk"
    }

text_path = "C:/Users/mathe/Documents/Github-repos/fitna-study/texts/0845Maqrizi.IghathaUmma.Kraken210223142017-ara1.dyn-tagged"
csv_out = "ighatha_famine_reasons.csv"
columns = ["insufficient_flood", "excessive_flood", "natural_other", "human"]

with open(text_path, encoding = "utf-8-sig") as f:
    text = f.read()
    f.close()

extract_head_dyn_loc(text, csv_out, columns, code_dict)