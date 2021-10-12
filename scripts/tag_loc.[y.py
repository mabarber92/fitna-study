# -*- coding: utf-8 -*-
"""
Created on Wed Mar 17 10:01:39 2021

@author: mathe
"""
import re

def tag_id (text, tag_type = []):
    text = re.sub("~~|#\s|\n", " ", text)
    text = re.sub("\s\s", " ", text)
    print(text)
    out_list = []
    for tag in tag_type:
        reg = tag + "(\d)"
        numbers = (re.findall(reg, text))
        max_str = max(numbers)
        
        for x in range(0, int(max_str)):
            regex = tag + str(x+1) + "((?:\s\S+){" + str(x+1) + "})"
            print(regex)
            found_list = re.findall(regex, text)
            print(found_list)
            for item in found_list:
                             
                out_list.append(item)
    print(out_list)
    freq_dict = {i:out_list.count(i) for i in out_list}
    print(freq_dict)
    
    text = re.sub("DES@\d@", "", text)
    length = len(text.split())
    print(length)
    
    
path = "C:/Users/mathe/Documents/Kitab project/ERC Vol/Chapter_redraft/Data/Fasl_Khitat_Famine"
    
with open(path, encoding = "utf-8") as f:
            text = f.read()
            f.close()
            
tag_id(text, ["@DES@"])