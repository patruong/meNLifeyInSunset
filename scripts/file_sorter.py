#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Sep  5 15:36:48 2020

@author: ptruong
"""

import os
import numpy as np
import pandas as pd


def sorted_files_parse():
    files = sorted(os.listdir())
    files_list = []
    for i in files:
        file_ext = i.split(".")[-1]
        decomp_str = i.split(".")[0].split("_")
        indexer = decomp_str[0]
        text = " ".join(decomp_str[1:-1])
        date = decomp_str[-1]
        obj = [indexer, text, date, file_ext]
        files_list.append(obj)
        
    df = pd.DataFrame(files_list, columns = ["indexer", "text", "date", "ext"])
    return df

sorted_files = sorted_files_parse()
sorted_files.to_csv("sorted_file_list.csv", sep = ",", index = False)
# read in file list
df = pd.read_csv("sorted_file_list.csv")


#def generate_list_to_sort(df):
#    df = df.drop("indexer",axis=1)
#    return df

def dump_list_to_sort(df):
    df.drop("indexer",axis=1).to_csv("file_list_to_sort.csv", sep =",", index = False)

dump_list_to_sort(df)
#generate_list_to_sort() #in scripts to get sorted list without index
#df2 = pd.read_csv("file_list_to_sort.csv")

# In gallery - remove indexes
def remove_index_from_gallery(df):
    """
    df should besorted_file_list and gallery should be sorted
    Outcome -> gallery will have indices removed
    """
    for i in range(len(df.index)):
        decomp = list(df[df.index == i].values[0])
        decomp[-2:] = [".".join(decomp[-2:])]
        init_str = decomp[0] + "_" + "_".join(decomp[1].split(" ")) + "_" + decomp[-1]
        end_str = "_".join(["_".join(decomp[1].split(" "))] + [decomp[-1]])
        os.rename(init_str, end_str)
        print("renamed: " + init_str + "->", end_str)

remove_index_from_gallery(df)

# ADD FILES AND THEN CONTINUE


df = pd.read_csv("file_list_to_sort.csv")

def remove_white_space_from_text(df):
    """
    removes the white space from text column - to correct for human mistakes
    """
    text_col_rm_white_space = []
    for i in df.text.values:
        text_col_rm_white_space.append(i.strip())
    
    df = pd.DataFrame(np.array([text_col_rm_white_space, df.date.values, df.ext.values]).T, columns = ["text", "date", "ext"])
    return df

df = remove_white_space_from_text(df)

# GO TO GALLERY TO REMOVE "_"

# Replace _ with white space and rename in folder (DONT USE)
for i in os.listdir():
    if "_" in i:
        new_str = i.replace("_", " ")
        os.rename(i, new_str)
        
# Replace ? with "" and rename file (DONT USE)
#for i in os.listdir():
#    if "?" in i:
#        new_str = i.replace("?", "")
#        os.rename(i, new_str)
#        print("renamed: " + i + "--->" + "new_str")

def index_file_list(df):
    """
    df should be unindexed file list with sorted pics
    """
    import string
    string.ascii_lowercase
    
    #a=[i for i in range(100)]
    file_list = list(df.values)[::-1]
    iterator = 0
    while True:
        try:
            iterator += 1
            for i in string.ascii_lowercase:
                print(str(iterator) + i)
                file_name_raw = list(file_list.pop())
                old_file_name = ".".join([" ".join(file_name_raw[:-1])] + [file_name_raw[-1]])
                file_name = "_".join(["_".join(file_name_raw[0].split(" "))] + [".".join(file_name_raw[1:])])
                new_file_name = "_".join([str(iterator) + i] + [file_name])
                try:
                    os.rename(old_file_name, new_file_name)
                    #print("renamed: " + old_file_name + "->", new_file_name)
                except:
                    print("WARNING BROKE AT " + old_file_name + " -> " + new_file_name)
                    print(i)
                    
                    return False
        except:
            print("Done!")
            break
    
index_file_list(df)
    
    
    
    
    
