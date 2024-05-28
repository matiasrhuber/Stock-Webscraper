import requests
import pickle
import json
import os
import yaml

### PARAMETERS ###
with open("SEC_config.yaml") as f:
    cfg = yaml.safe_load(f)

SEC_user_agent = cfg['SEC_user_agent']
encoding = cfg['encoding']
host = cfg['host']
SEC_headers = {'User-Agent': SEC_user_agent,'Accept-Encoding':'gzip','Host':host} #cfg['SEC_headers']
CIK = '320193'
years = range(cfg['years']['start'],cfg['years']['end'])
params = cfg['params'] 

curr_dir = os.getcwd()
folder = 'SEC'
###############################


# Ticker and CIK mapping
tickers_cik = requests.get("https://www.sec.gov/files/company_tickers.json",headers=SEC_headers)
tickr_text = tickers_cik.text
# print(tickr_text)
tickr_dict = json.loads(tickr_text)

for num in range(len(tickr_dict)):
    tickr_dict[(tickr_dict[str(num)]["ticker"])] = tickr_dict[str(num)]
    del tickr_dict[str(num)]

with open(os.path.join(curr_dir,folder,"cik_tickr_mapping.pkl"),"wb") as f:
    pickle.dump(tickr_dict, f)

