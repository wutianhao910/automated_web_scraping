# -*- coding: utf-8 -*-
"""
Created on Thu Jun 21 18:11:59 2018

@author: Valar Morghulis
"""

#不用spyder的原因是因为flickrapi在spyder上有bug，在github上有人问过
import flickrapi
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

def get_geo(df_pic,file_name,api_key,api_secret):
    st = time.clock()
    file_name = file_name.replace('id','geo')
    df_info = pd.DataFrame(columns=['pic_id','latitude','longitude','county','region','country'])
    df_info.to_csv(file_name,sep=',',index=None)
    total = 0
    amount = 0
    drop_nan = 0
    
    for i in range(len(df_pic.index)):
        
        if amount < 100000:
            try:
                flickr=flickrapi.FlickrAPI(api_key,api_secret,format='parsed-json')
                pic_geo = flickr.photos.geo.getLocation(photo_id=df_pic['pic_id'].iloc[i])
                geo = pic_geo['photo']['location']
                
                for loc in geo:
                    if loc == 'latitude':
                        df_info[loc] = pd.Series(geo[loc])
                    if loc == 'longitude':
                        df_info[loc] = pd.Series(geo[loc])
                    if loc == 'county':
                        df_info[loc] = pd.Series(geo[loc]['_content'])
                    if loc == 'region':
                        df_info[loc] = pd.Series(geo[loc]['_content'])
                    if loc == 'country':
                        df_info[loc] = pd.Series(geo[loc]['_content'])
                        
                amount += 1
                df_info['pic_id'] = df_pic['pic_id'].iloc[i]
                df_info.to_csv(file_name,sep=',',index=None,header=None,mode='a')
            except:
                drop_nan += 1
                pass
            
        total += 1
        st_info = round(time.clock()-st,2)
        print('\rGETTING GEO: {0} , DROP_NAN: {1} , TOTAL: {2} , TIME CONSUMED: {3}s'.format(amount,drop_nan,total,st_info),end='',flush=True)
        #time.sleep(1)
    dline(2)
    print('FILE: %s SAVED !' %file_name)
    print('SIZE: %i' %amount)
 
api_key = '404afab90a2381ab68c53efba4d3cb44'
api_secret = 'e13d4f79198b64c7'
root = 'D:/Dropbox/WCD_BootCamp/Project_0_Flickr/Data'

path = mkdir(root,'IDs_Views')
csv_lst = list(os.walk(path))[0][2]
path = mkdir(root,'Geo')

for id_csv in csv_lst:  
    
    file_path = path + '/' + id_csv.replace('id','exif')
    exist = os.path.exists(file_path)
    
    if exist:
        print('FILE: %s ALREADY ABSORBED !' %id_csv)
        pass
    else:
        print('CRAWLING ON : %s...' %id_csv)
        dline(0)
        
        mkdir(root,'IDs_Views')
        df_pic = pd.read_csv(id_csv,sep=',',engine='python')
        df_pic.columns = ['pic_id','Views','tag']
        df_pic = df_pic.drop_duplicates().sort_values('Views',ascending=False).reset_index()
        del df_pic['index']
        
        path = mkdir(root,'Geo')
        get_geo(df_pic,id_csv,api_key,api_secret)
        dline(1)
print('FINISH !!!')