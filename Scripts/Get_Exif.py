# -*- coding: utf-8 -*-
"""
Created on Thu Jun 21 14:21:48 2018

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

#Get Exif info
def get_exif(df_pic,file_name,api_key,api_secret):
    st = time.clock()
    file_name = file_name.replace('id','exif')
    df_info = pd.DataFrame(columns=['pic_id','Camera_Make','Camera_Model',
                                    'Exposure','Aperture','Exposure_Program',
                                    'ISO','Metering_Mode','Flash','Focal_Length',
                                    'Color_Space','Lens_Model'])
    df_info.to_csv(file_name,sep=',',index=None)
    total = 0
    amount = 0
    drop_nan = 0
        
    for i in range(len(df_pic.index)):
            
        if amount < 100000:
            try:
                flickr=flickrapi.FlickrAPI(api_key,api_secret,format='parsed-json')
                exif = flickr.photos.getExif(photo_id=df_pic['pic_id'].iloc[i])
                
                for info in exif['photo']['exif']:
                    if info['label'] == 'Make':
                        df_info['Camera_Make'] = pd.Series(info['raw']['_content'])
                    elif info['label'] == 'Model':
                        df_info['Camera_Model'] = pd.Series(info['raw']['_content'])
                    elif info['label'] == 'Exposure':
                        if '/' in info['raw']['_content']:
                            operator = info['raw']['_content'].strip().split('/')
                            df_info['Exposure'] = pd.Series(float(operator[0])/float(operator[1]))
                        else:
                            df_info['Exposure'] = pd.Series(float(info['raw']['_content'].strip()))
                    elif info['label'] == 'Aperture':
                        df_info['Aperture'] = pd.Series(float(info['raw']['_content'].strip()))
                    elif info['label'] == 'Exposure Program':
                        df_info['Exposure_Program'] = pd.Series(info['raw']['_content'])
                    elif info['label'] == 'ISO Speed':
                        df_info['ISO'] = pd.Series(float(info['raw']['_content'].strip()))
                    elif info['label'] == 'Metering Mode':
                        df_info['Metering_Mode'] = pd.Series(info['raw']['_content'])
                    elif info['label'] == 'Flash':
                        df_info['Flash'] = pd.Series(info['raw']['_content'])
                    elif info['label'] == 'Focal Length':
                        df_info['Focal_Length'] = pd.Series(float(info['raw']['_content'].replace('mm','').strip()))
                    elif info['label'] == 'Color Space':
                        df_info['Color_Space'] = pd.Series(info['raw']['_content'])
                    elif info['label'] == 'Lens Model':
                        df_info['Lens_Model'] = pd.Series(info['raw']['_content'])
                
                df_info['pic_id'] = df_pic['pic_id'].iloc[i]
                df_info.to_csv(file_name,sep=',',index=None,header=None,mode='a')
                amount += 1
            except Exception as e:
                drop_nan += 1
                pass
            
        else:
            break
        total += 1
        st_info = round(time.clock()-st,2)
        print('\rGETTING INFO: {0} , DROP_NAN: {1} , TOTAL: {2} , TIME CONSUMED: {3}s'.format(amount,drop_nan,total,st_info),end='',flush=True)
        #time.sleep(1)
    dline(2)
    print('FILE: %s SAVED !' %file_name)
    print('SIZE: %i' %amount)
    
    return

api_key = '2b74061345250898719cdc9cf9aae8f0'
api_secret = '0825a78a0bd5865e'
root = 'D:/Dropbox/WCD_BootCamp/Project_0_Flickr/Data'

path = mkdir(root,'IDs_Views')
csv_lst = list(os.walk(path))[0][2]
path = mkdir(root,'Exif')
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
        
        path = mkdir(root,'Exif')
        get_exif(df_pic,id_csv,api_key,api_secret)
        dline(1)
print('FINISH !!!')