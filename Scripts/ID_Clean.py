# -*- coding: utf-8 -*-
"""
Created on Sun Jun 24 18:28:44 2018

@author: Tianhao Wu
"""

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

root = 'D:\Dropbox\WCD_BootCamp\Project_0_Flickr\Data'
path = mkdir(root,'IDs_Views')
csv_lst = list(os.walk(path))[0][2]
df_id = pd.DataFrame()

for csv in csv_lst:
    df = pd.DataFrame()
    df = pd.read_csv(csv,sep=',',engine='python')
    df.columns = ['pic_id','Views','tag']
    tag = df['tag'].iloc[0]
    print('COLUMNS ATTACHED TO: %s' %csv)
    df = df.drop_duplicates()
    print('REMAINING:',len(df.index))
    dline(2)
    df = df.groupby('pic_id').sum()
    df['tag'] = tag
    df = df.sort_values('Views',ascending=False).reset_index()
    
    print(df.head())
    dline(2)
    print('DUPLICATES DROPED: %s' %csv)
    print('REMAINING:',len(df.index))
    dline(2)
    path = mkdir(root,'IDs_Views_Cleaned')
    df.to_csv(csv,sep=',',index=None)
    path = mkdir(root,'IDs_Views')
    df_id = pd.concat([df_id,df])
    print('MERGED: %s' %csv)
    dline(1)

mkdir(root)
df_id.to_excel('ID_Merged.xlsx',index=None)
print('ID CLEAND !!!')