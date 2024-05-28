import requests
import os
import numpy as np
import json
import yaml

### PARAMETERS ###
with open("SEC_config.yaml") as f:
    cfg = yaml.load(f)

SEC_user_agent = cfg['SEC_user_agent']
encoding = cfg['encoding']
host = cfg['host']
SEC_headers = {'User-Agent': SEC_user_agent,'Accept-Encoding':'gzip','Host':host} #cfg['SEC_headers']
years = range(cfg['years']['start'],cfg['years']['end'])
params = cfg['params'] 
quarters = cfg['quarters']

base_url = 'https://www.sec.gov/Archives/edgar/full-index/'
#######################################

# Index for file locations of 10-k and 10-q filings

for year in years:
    try:
        os.mkdir(f'./SEC/Master_Index/{year}')
    except:
        print(f'Previous data from year {year} already saved')
    for q in quarters:
        print(f'Going through files from {year} {q}...')
        master_index = requests.get(base_url+f'{year}/{q}/master.idx', headers=SEC_headers).text
        master_index = master_index.split('--------------------------------------------------------------------------------')[1]

        master_index = master_index.replace('\n','|').split('|')
        del master_index[0]
        keys = master_index[::5]
        del master_index[::5]

        # Fit data into dictionary and select only 10-k and 10-q file types
        shape = int(len(master_index)/4)
        print(f'File size for {year} {q}: {shape}')
        
        data = np.array(master_index).reshape(shape,4)
        cols = ['Company Name', 'Form Type', 'Date Filled', 'File Name']
        dict_master = {}
        for set,key in zip(data,keys):
            dict_temp = {key:value for (key,value) in zip(cols,set)}
            if dict_temp['Form Type'] == '10-K':
                dict_master[key+'_10-k'] = dict_temp
            if dict_temp['Form Type'] == '10-Q':
                dict_master[key+'_10-q'] = dict_temp
        print(f'10-K or 10-Q Filings saved: {len(dict_master)}')
        
        with open(f'./SEC/Master_Index/{year}/{q}.txt','w') as f:
            f.write(json.dumps(dict_master))