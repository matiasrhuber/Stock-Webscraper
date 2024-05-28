import json
import requests
from bs4 import BeautifulSoup
import os
import pickle as pkl
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
stocks = cfg['stocks']

file_types = ['_10-q','_10-k']
base_url = 'https://www.sec.gov/Archives/'
curr_dir = os.getcwd()
folder = 'SEC'

base_url = 'https://www.sec.gov/Archives/'
#######################################


with open(os.path.join(folder, 'cik_tickr_mapping.pkl'), 'rb') as f:
    tickr_dict = pkl.load(f) # deserialize using load()


for year in years:
    for quarter in quarters:
        with open(f'./SEC/Master_Index/{year}/{quarter}.txt','r') as f: 
            text = f.read()
        dict_ind = json.loads(text)
        
        for stock in stocks:
            try: 
                os.mkdir(os.path.join(curr_dir,folder,stock))
            except:
                pass
            cik = tickr_dict[stock]['cik_str']
            try:
                file_type = file_types[0] # Quarterly Filings
                url = dict_ind[str(cik)+file_type]['File Name'].replace('-','').replace('.txt','')
            except:
                file_type = file_types[1] # Yearly Filings
                try:
                    url = dict_ind[str(cik)+file_type]['File Name'].replace('-','').replace('.txt','')
                except KeyError:
                    print(f'No data found for {stock} {year} {quarter}')
                    continue
            file = '/FilingSummary.xml'
            data = requests.get(base_url+url+file,headers=SEC_headers).content
            soup = BeautifulSoup(data, 'lxml')
            myreports = soup.find('myreports')

            if myreports is None:
                print(f'Empty report for {stock} {year} {quarter}')
                continue
                # soup = BeautifulSoup(data, 'xml')
                # myreports = soup.find('myreports')
                # print('soup:',soup)
                
            # List with individual components from myreports
            master_reports = []
            print(f'Gathering data for {stock}{file_type} @ {quarter} {year}')
            for report in myreports.find_all('report')[:-1]:

            # dictionary with all relevant parts
                report_dict = {}
                
                try:
                    report_dict['name_short'] = report.shortname.text
                    report_dict['name_long'] = report.longname.text
                    report_dict['position'] = report.position.text
                    report_dict['category'] = report.menucategory.text
                    report_dict['url'] = base_url + url + '/' + report.htmlfilename.text
                    master_reports.append(report_dict)
                except AttributeError:
                    print(f'Lack of data in the report for {stock} {year} {quarter}')
            
            try: 
                os.mkdir(os.path.join(curr_dir,folder,stock,'master_reports'))
            except:
                print('Saving master report along existing data {}'.format(stock))


            
            with open(os.path.join(curr_dir,folder,stock,'master_reports',f'master_reports_{file_type}_{year}_{quarter}.json'), 'w') as fout:
                json.dump(master_reports , fout)