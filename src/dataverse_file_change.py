# -*- coding: utf-8 -*-
"""
Created on Wed May 22 12:29:27 2024

@author: rabni
"""
from pyDataverse.api import NativeApi, DataAccessApi
import os
import requests  # http://docs.python-requests.org/en/master/
import json
import netCDF4 as nc
import numpy as np
import zipfile 
import pandas as pd
from nco import Nco
nco = Nco()
# Setup Dataverse connection
dataverse_server = 'https://dataverse.geus.dk'
api_key = 'e4d37615-8a58-4d9a-a865-4a15f9038a66' # Youe GEUS Dataverse API KEY
downloadId = 'doi:10.22008/FK2/FBIFOX'
uploadId = 'doi:10.22008/FK2/RTFM0K'

api = NativeApi(dataverse_server, api_key)
data_api = DataAccessApi(dataverse_server, api_key)

dataset = api.get_dataset(downloadId)
files_dataverse = dataset.json()['data']['latestVersion']['files']

dataset_upload = api.get_dataset(uploadId)
files_dataverse_upload = dataset_upload.json()['data']['latestVersion']['files']

url_persistent_id = '%s/api/datasets/:persistentId/add?persistentId=%s&key=%s' % (dataverse_server, uploadId, api_key)
re = 'Greenland'
# Directory to store downloaded files
base_f =  r'C:\Users\rabni\OneDrive - GEUS\Skrivebord\SICE_get\files_to_replace'
download_dir = base_f + os.sep + re + os.sep + 'nc'
zip_folder = base_f + os.sep + re + os.sep + 'zipped'
os.makedirs(download_dir, exist_ok=True)

o = 'BBA_combination'
long = 'combination of corrected broadband albedo'
unit = 'unitless'

thresh_bare_ice = 0.565
a = 1.003
b = 0.058
start_d ='2021-06-01'
end_d = '2021-10-01'
dates_period = pd.date_range(start=start_d,end=end_d).to_pydatetime().tolist()
dates_period = [d.strftime("%Y-%m-%d") for d in dates_period]

def BBA_combination(nc_file):
    
    ds = nc.Dataset(nc_file, "r+", format="NETCDF4")

    if o not in list(ds.variables.keys()): 
        alb = np.array(ds['albedo_bb_planar_sw'])
        BBA_combo = np.ones_like(alb) * np.nan

        b01 = np.array(ds['r_TOA_01'])
        b06 = np.array(ds['r_TOA_06'])
        b17 = np.array(ds['r_TOA_17'])
        b21 = np.array(ds['r_TOA_21'])

        temp = np.array(a * ((b01 + b06 + b17 + b21) / 4) + b)

        v = temp <= thresh_bare_ice
        BBA_combo[v] = temp[v]

        v = temp > thresh_bare_ice
        BBA_combo[v] = alb[v]

        inv = BBA_combo > 0.95
        BBA_combo[inv] = np.nan

        inv = BBA_combo < 0.058
        BBA_combo[inv] = np.nan

        z_out = ds.createVariable(o, 'f4', ('y', 'x'),zlib=True)
        z_out[:,:] = BBA_combo
        z_out.standard_name = o
        z_out.long_name = long
        z_out.units = unit
        
    
    ds.close()
    
    return 


# def zip_nc(file_path,zip_path):
#     # Get the NetCDF filename to store in the zip archive
#     netcdf_filename = os.path.basename(file_path)
    
#     nco.ncks(input=file_path, output=zip_path + os.sep + netcdf_filename, options=['-7 -L 1'])
    
#     # with zipfile.ZipFile(zip_path, 'a', zipfile.ZIP_DEFLATED) as zipf:
#     #     zipf.write(file_path, arcname=netcdf_filename)
#     return

# Function to download a file
def download_file(f_id,f_name):
   
    print(f'downloading {f_name}')
    response = data_api.get_datafile(f_id)
    
    f_name_local = download_dir + os.sep + f_name
    with open(f_name_local, "wb") as f:
        f.write(response.content)
        
    return f_name_local

def upload_file(file_id,local_file,desc,label):
    
    
    #url_persistent_id = '%s/api/files/%s/replace?persistentId=%s&key=%s' % (dataverse_server, file_id,persistentId, api_key)
    #print(url_persistent_id)
    fileup = {'file': open(local_file, "rb")}
    
    params = dict(description=desc,
                       directoryLabel=label)
    
    params_as_json_string = json.dumps(params)

    payload = dict(jsonData=params_as_json_string)
    
    r = requests.post(url_persistent_id,data = payload, files=fileup)
   
    
    return r
    

# Rename files

#files_dataverse = files_dataverse[30:]

upload_files = [file['dataFile']['filename'] for file in files_dataverse_upload] 
date_uploads = [f[-13:-3] for f in upload_files] 

ll = 0


for file in files_dataverse:
    
    file_id = file['dataFile']['id']
    original_filename = file['dataFile']['filename']
    output_tag = file['dataFile']['description'].split(' ')[3][:-1]
    date = original_filename[-13:-3]
    date = date.replace('_','-')
    if original_filename == output_tag:
        if date in dates_period:
            
         
            new_filename = f'SICEv3.0_{re}_500m_{date}.nc'  # Modify this to your desired new filename
            new_description =  f"EDC SICE output: {new_filename}, date: {date}"
            new_directory_label = f"{date}"
            
            f_name_local = download_file(file_id,new_filename)
            #BBA_combination(f_name_local)
            #zip_nc(f_name_local,zip_folder)
            # r = upload_file(file_id,f_name_local, new_description, new_directory_label)
            
            # #print(r.json()['status'])
            
            # os.remove(f_name_local)
        
        