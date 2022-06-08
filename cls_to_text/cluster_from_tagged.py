# -*- coding: utf-8 -*-
"""
Created on Mon May 23 11:45:27 2022

@author: mathe
"""
import pandas as pd
import re
import pyarrow.parquet as pq
import os
from tqdm import tqdm
from openiti.helper.funcs import text_cleaner

def cluster_from_tagged(meta_path, tagged_texts, tags, out_dest, parquet_path = "", results_csv = "results_cl.csv", no_cl_csv = "no_cluster_list.csv", existing_cl = None, max_date = 900, cluster_cap = 500, 
                        safe_tags = ["\n# ", "\n### | ", "\n### || ", "\n### ||| ", "\n### |||| ", "\n### ||||| ", "\n~~"]):
    """
    """
    # If a variable is passed in - take that as cl data
    if existing_cl is not None:
        all_cls = existing_cl.copy()
        print("Using existing data... skipping to tagging")
    
    # Otherwise load from parquets from supplied path
    else:
        os.chdir(parquet_path)
        all_cls = pd.DataFrame()
        for root, dirs, files in os.walk(".", topdown=False):
            for name in tqdm(files):
                pq_path = os.path.join(root, name)            
                data = pq.read_table(pq_path).to_pandas()[["cluster", "size", "seq", "series", "text", "begin", "end"]]
                data = data[data["size"] < cluster_cap]

                all_cls = pd.concat([all_cls, data])
    
    
    
    # Use metadata to filter according to requirements
    # Add book URI to make easier to read outputs
        meta_df = pd.read_csv(meta_path, sep="\t")[["id", "book", "date"]]
        all_cls["id"] = all_cls["series"].str.split("-").str[0]
        all_cls = pd.merge(all_cls, meta_df, how = "inner", on ="id")
    
        print("New cluster data loaded...")
    
        # Applying the date filter to output
        all_cls = all_cls[(all_cls["date"] <= max_date)]
        all_cls = all_cls.drop(columns = ["date"])
    
        print("Cluster data filtered...")
    
    # Switch wd to script dir
    # abspath = os.path.abspath(__file__)
    # dname = os.path.dirname(abspath)
    # os.chdir(dname)
    
    # Collect cluster data for each text and insert tags
    for root, dirs, files in os.walk(tagged_texts, topdown=False):
            for name in tqdm(files):
                # Get subset of cluster data relevant to text in question
                text_id = name.split(".")[-1].split("-")[0]
                data_subset = all_cls[all_cls["id"] == text_id]
                clusters_for_text_df = pd.DataFrame()
                no_clusters = []
                
                text_path = os.path.join(root, name)
                print(text_path)
                with open(text_path, encoding = "utf-8") as f:
                    text = f.read()
                    f.close()
                # Split text into milestones and find those with tags - Need to split and retain a milestone ID, then
                # need to go through splits, find tagged ones, grap ms number and create a unique Id - URI+COUNT, OpenITI normalise,
                # find clusters and insert tags, output to csv, save text
                text = re.split(r"(ms\d+)", text)
                final_text = text[:]
                result_count = 0
                for idx, ms_section in enumerate(text):
                    for tag in tags:
                        if re.search(tag, ms_section) is not None:
                            result_id = name + "." + str(result_count)
                            result_count = result_count + 1
                            ms_int = int(text[idx+1].lstrip("ms"))
                            
                            
                            
                            
                            
                            
                            
                            # Get and tag data for ms
                            
                            clusters = data_subset[data_subset["seq"] == ms_int].to_dict("records")
                            
                            if len(clusters) > 0:
                                
                                tagidxs_dict = []
                                for each_tag in tags:
                                    tempsplits = re.split(each_tag, ms_section)
                                    
                                    for tidx, tempsplit in enumerate(tempsplits[:-1]):
                                        indexpos = len(text_cleaner(" ".join(tempsplits[0:tidx+1])))
                                        tagidxs_dict.append({"tag": each_tag, "index": indexpos, "tagged": False})
                                
                            
                                for safe_tag in safe_tags:
                                    tempsplits = ms_section.split(safe_tag)
                                    
                                    for tidx, tempsplit in enumerate(tempsplits[:-1]):
                                        indexpos = len(text_cleaner(" ".join(tempsplits[0:tidx+1])))
                                        tagidxs_dict.append({"tag": safe_tag, "index": indexpos, "tagged": False})
                            
                                tagidxs_dict = pd.DataFrame(tagidxs_dict).sort_values(by = ["index"]).to_dict("records")    
                                
                                
                                
                                
                                new_ms_text = text_cleaner(ms_section[:])
                                
                                mapping_dict = []
                                for cluster in clusters:
                                    
                                    mapping_dict.append({"cluster": cluster["cluster"], "type" : " @clb@" + str(cluster["size"]) + "@", "index" : cluster["begin"]})
                                    mapping_dict.append({"cluster": cluster["cluster"], "type" : " @cle@", "index" : cluster["end"]})
                                    
                                    cluster_df = all_cls[all_cls["cluster"] == cluster["cluster"]]
                                    
                                    cluster_df.insert(0, "result_id", result_id)
                                    clusters_for_text_df = pd.concat([clusters_for_text_df, cluster_df])
                                    
                                    
                                mapping_dict = pd.DataFrame(mapping_dict).sort_values(by = ["index"]).to_dict("records")    
                                
                                offset = 0
                                tagged_count = 0
                                total_tags = len(tagidxs_dict)
                                for mapping in mapping_dict:
                                    reusetag = mapping["type"] + str(mapping["cluster"]) + "@ "
                                    index = mapping["index"]
                                    if tagged_count != total_tags:
                                        for tagidx in tagidxs_dict:
                                            if tagidx["index"] < index and tagidx["tagged"] is False:
                                                new_ms_text = new_ms_text[: tagidx["index"] + offset] + tagidx["tag"] + new_ms_text[tagidx["index"] + offset :]
                                                offset = offset + len(tagidx["tag"])
                                                tagidx["tagged"] = True                                               
                                                tagged_count = tagged_count + 1
                                    new_ms_text = new_ms_text[: mapping["index"] + offset] + reusetag + new_ms_text[mapping["index"] + offset :]
                                    offset = offset + len(reusetag)
                                if tagged_count != total_tags:
                                    for tagidx in tagidxs_dict:
                                        if tagidx["tagged"] is False:
                                            new_ms_text = new_ms_text[: tagidx["index"] + offset] + tagidx["tag"] + new_ms_text[tagidx["index"] + offset :]
                                            tagidx["tagged"] = True
                                            offset = offset + len(tagidx["tag"])
                                            
                                # Replace the milestone with the tagged version in the final file
                                final_text[idx] = new_ms_text
                                
                               
                           
                            else:
                                no_clusters.append([result_id, text[idx+1]])
                                
                            
                            # Repeat whole task for next ms
                            following_ms = ms_int + 1
                            
                            clusters = data_subset[data_subset["seq"] == following_ms].to_dict("records")
                            
                            if len(clusters) > 0:
                                ms_string = text[idx+2]
                                
                                tagidxs_dict = []
                                for each_tag in tags:
                                    tempsplits = re.split(each_tag, ms_string)
                                    
                                    for tidx, tempsplit in enumerate(tempsplits[:-1]):
                                        indexpos = len(text_cleaner(" ".join(tempsplits[0:tidx+1])))
                                        tagidxs_dict.append({"tag": each_tag, "index": indexpos, "tagged": False})
                                
                            
                                for safe_tag in safe_tags:
                                    tempsplits = ms_string.split(safe_tag)
                                    
                                    for tidx, tempsplit in enumerate(tempsplits[:-1]):
                                        indexpos = len(text_cleaner(" ".join(tempsplits[0:tidx+1])))
                                        tagidxs_dict.append({"tag": safe_tag, "index": indexpos, "tagged": False})
                            
                                tagidxs_dict = pd.DataFrame(tagidxs_dict).sort_values(by = ["index"]).to_dict("records")    
                                
                                
                                
                                
                                new_ms_text = text_cleaner(ms_string[:])
                                
                                mapping_dict = []
                                for cluster in clusters:
                                    
                                    mapping_dict.append({"cluster": cluster["cluster"], "type" : " @clb@" + str(cluster["size"]) + "@", "index" : cluster["begin"]})
                                    mapping_dict.append({"cluster": cluster["cluster"], "type" : " @cle@", "index" : cluster["end"]})
                                    
                                    cluster_df = all_cls[all_cls["cluster"] == cluster["cluster"]]
                                    
                                    cluster_df.insert(0, "result_id", result_id)
                                    clusters_for_text_df = pd.concat([clusters_for_text_df, cluster_df])
                                    
                                mapping_dict = pd.DataFrame(mapping_dict).sort_values(by = ["index"]).to_dict("records")    
                                
                                offset = 0
                                tagged_count = 0
                                total_tags = len(tagidxs_dict)
                                for mapping in mapping_dict:
                                    reusetag = mapping["type"] + str(mapping["cluster"]) + "@ "
                                    index = mapping["index"]
                                    if tagged_count != total_tags:
                                        for tagidx in tagidxs_dict:
                                            if tagidx["index"] < index and tagidx["tagged"] is False:
                                                new_ms_text = new_ms_text[: tagidx["index"] + offset] + tagidx["tag"] + new_ms_text[tagidx["index"] + offset :]
                                                offset = offset + len(tagidx["tag"])
                                                tagidx["tagged"] = True                                               
                                                tagged_count = tagged_count + 1
                                    new_ms_text = new_ms_text[: mapping["index"] + offset] + reusetag + new_ms_text[mapping["index"] + offset :]
                                    offset = offset + len(reusetag)
                                if tagged_count != total_tags:
                                    for tagidx in tagidxs_dict:
                                        if tagidx["tagged"] is False:
                                            new_ms_text = new_ms_text[: tagidx["index"] + offset] + tagidx["tag"] + new_ms_text[tagidx["index"] + offset :]
                                            tagidx["tagged"] = True
                                            offset = offset + len(tagidx["tag"])
                                # Replace the milestone with the tagged version in the final file
                                final_text[idx+2] = new_ms_text            
                                
                           
                            else:
                                no_clusters.append([result_id, text[idx+3]])
                               
                            break
                
                clusters_for_text_df["cluster"] = clusters_for_text_df["cluster"].astype(str)
                final_text = "".join(final_text)
                no_clusters_df = pd.DataFrame(no_clusters, columns = ["result_id", "milestone"])
                
                out_path_text = os.path.join(out_dest, name) + ".cl-tagged"
                out_path_csv = os.path.join(out_dest, name) + "_clusters.csv"
                out_path_nocl = os.path.join(out_dest, name) + "_no-clusters.csv"
                with open(out_path_text, "w", encoding = "utf-8") as f:
                    f.write(final_text)
                    f.close()
                
                clusters_for_text_df.to_csv(out_path_csv, encoding = 'utf-8-sig', index = False)
                no_clusters_df.to_csv(out_path_nocl, index = False)
                            
                            
                            
                        
                        # Get and tag data for following ms
                        # print(ms_int + 1)
                        # clusters = data_subset[data_subset["seq"] == ms_int + 1]
                        # print(clusters)
    
    return(all_cls)
                        
path = "D:/Corpus Stats/2021/Cluster data/Oct_2021/parquet/"
test_path = "D:/Corpus Stats/2021/Cluster data/Oct_2021/test"
meta_path = "D:/Corpus Stats/2021/OpenITI_metadata_2021-2-5_merged_wNoor.csv"
text_path = "C:/Users/mathe/Documents/Github-repos/fitna-study/cls_to_text/texts"
out_path = "C:/Users/mathe/Documents/Github-repos/fitna-study/cls_to_text/outputs2/"

clusters = cluster_from_tagged(meta_path, text_path, ["@ST0@tr@"], out_path, path)