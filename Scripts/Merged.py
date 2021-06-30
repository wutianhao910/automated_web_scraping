# -*- coding: utf-8 -*-
"""
Created on Wed Jun 27 09:32:50 2018

@author: Valar Morghulis
"""

import numpy as np
import pandas as pd
import os

def dline(operator):
    if operator == 0:
        print('- - - - - - - - - - - - - - - - - - - - - - - - - - - - -')
    elif operator == 1:
        print('----------------------------------------------------------------------------------')
    elif operator == 2:
        print('- - - - - - - - - - - - -')
    return

def mkdir(root,folder=''):
    path = root+'/'+folder
    folder = os.path.exists(path)
    if not folder:
        os.makedirs(path)
        os.chdir(path)
    else:
        os.chdir(path)
        pass
    return path

def read_csv(root,folder):
    path = mkdir(root,folder)
    csv_lst = list(os.walk(path))[0][2]
    df_merge = pd.DataFrame()
    
    for csv in csv_lst:
        df = pd.DataFrame()
        df = pd.read_csv(csv,sep=',',engine='python')        
        dline(2)
        df_merge = pd.concat([df_merge,df])
        print('MERGED: %s' %csv)
    dline(1)
    return df_merge

root = 'D:\Dropbox\WCD_BootCamp\Project_0_Flickr\Data'
df_id = read_csv(root,'IDs_Views_Cleaned')
df_exif = read_csv(root,'Exif').drop_duplicates()
df_geo = read_csv(root,'Geo').drop_duplicates()

df_merge = pd.merge(df_id,df_exif,on=['pic_id','pic_id'],how='left')
df_merge = pd.merge(df_merge,df_geo,on=['pic_id','pic_id'],how='left')

mkdir(root)
df_merge.fillna(np.nan,inplace=True)
df_merge.to_csv('Merged.csv',sep=',',index=None)
print(df_merge.head())
