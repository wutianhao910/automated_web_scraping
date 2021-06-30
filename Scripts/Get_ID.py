# -*- coding: utf-8 -*-
"""
Created on Thu Jun 21 13:49:29 2018

@author: Valar Morghulis
"""

#不用spyder的原因是因为flickrapi在spyder上有bug，在github上有人问过
import requests
import flickrapi
from bs4 import BeautifulSoup
import pandas as pd
import time
import os

def dline(operator):
    if operator == 0:
        print('- - - - - - - - - - - - - - - - - - - - - - - - - - - - -')
    elif operator == 1:
        print('----------------------------------------------------------------------------------')
    elif operator == 2:
        print('\n- - - - - - - - - - - - - - - - - - - - - - - - - - - - -')
    return

#create folder path
def mkdir(root,folder):
    path = root+'/'+folder
    folder = os.path.exists(path)
    if not folder:
        os.makedirs(path)
        os.chdir(path)
    else:
        os.chdir(path)
        pass
    return path

#get tags
def get_tags(url_base):
    res = requests.get(url_base + '/photos/tags')
    res.encoding = 'utf-8'
    hsoup = BeautifulSoup(res.text,'html.parser')
    
    tag_lst = []
    for tag in hsoup.select('.overlay'):
        tag_lst.append(tag.text)
    for i in range(len(tag_lst)):
        if tag_lst[i] == 'sunset':
            tag_lst = tag_lst[i:][:10]
            print('TAG_LIST ABSORBED !')
            print(tag_lst)
            dline(1)
            break
    time.sleep(0.5)
    return tag_lst

#Get photo id
def get_pic(tag,min_date,api_key,api_secret):
    st = time.clock()
    flickr=flickrapi.FlickrAPI(api_key,api_secret,cache=True)      
    
    try:
        photos=flickr.walk(tags=tag,sort='interestingness-desc',content_type='1',extras='views',min_upload_date=min_date)
    except Exception as e:
        print('get_pic()',e)
    
    file_name = tag + '_id.csv'
    df_pic = pd.DataFrame(columns=['pic_id','Views','tag'])
    df_pic.to_csv(file_name,sep=',',index=None)
    total = 0
    amount = 0
    drop_nan = 0
    
    for photo in photos:
            
        exist = (float(str(photo.get('views').strip()))!= 0)
        if exist:
            df_pic['pic_id'] = pd.Series(str(photo.get('id')))
            df_pic['Views'] = pd.Series(float(str(photo.get('views').strip())))
            amount += 1
        else:
            drop_nan += 1
        
        df_pic['tag'] = tag
        df_pic.to_csv(file_name,sep=',',index=False,header=None,mode='a')
        df_pic = pd.DataFrame()
        
        total += 1
        st_pic = round(time.clock() - st,2)
        print('\rGETTING PICS: {0} , DROP_NAN: {1} , TOTAL: {2} , TIME CONSUMED: {3}s'.format(amount,drop_nan,total,st_pic),end='',flush=True)
        #time.sleep(1)
        if amount >= 20:
            break
        else:
            pass
    print('\nPIC_SET: %s SAVED !' %tag)
    dline(1)
    return

url_base = 'https://www.flickr.com'
api_key = 'e6b00be365cab3b2c004788b12bb6b47'
api_secret = '401e90577d12f507'
root = 'D:/Dropbox/WCD_BootCamp/Project_0_Flickr/Data'
min_date = '2018-01-01'
tag_lst = get_tags(url_base)

for tag in tag_lst:
    path = mkdir(root,'IDs_Views')
    file_path = path + '/' + tag + '_id.csv'
    exist = os.path.exists(file_path)

    if exist:
        print('TAG: %s ALREADY ABSORBED !' %tag)
        pass
    else:
        print('CRAWLING ON TAG: %s...' %tag)
        dline(0)
        get_pic(tag,min_date,api_key,api_secret)
print('FIINISH !!!')