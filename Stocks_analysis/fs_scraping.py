import os
import json
import yaml
import requests
from bs4 import BeautifulSoup

### PARAMETERS ###
with open("SEC_config.yaml") as f:
    cfg = yaml.load(f)


SEC_user_agent = cfg['SEC_user_agent']
encoding = cfg['encoding']
host = cfg['host']
SEC_headers = {'User-Agent': SEC_user_agent,'Accept-Encoding':'gzip','Host':host} #cfg['SEC_headers']
financial_statements_mapping = cfg['financial_statements_mapping']
stocks = cfg['stocks'] #['GOOGL','AAPL','TSLA','AMZN','META', 'SNAP']
file_types = ['_10-q','_10-k']
quarters = cfg['quarters']
years = range(cfg['years']['start'],cfg['years']['end'])
curr_dir = os.getcwd()
folder = 'SEC'
###############################

statements_url = []
missing_data_ls = [] 
num_missing = 0

# Saves url of desired financial statements, and checks for missing data due to improper mapping
for stock in stocks:
    try:
        os.mkdir(os.path.join(curr_dir,folder,stock,'financial_statements_url'))
    except:
        print('...previous urls already exist...')
    try:
        os.mkdir(os.path.join(curr_dir,folder,stock,'financial_statements_raw'))
    except:
        print('...previous raw data already exist...')
    try:
        os.mkdir(os.path.join(curr_dir,folder,stock,'master_reports'))
    except:
        print('...previous master report already exist...')
        
    for year in years:
        for quarter in quarters:
            print('*'*100)
            print(f'{stock} {year} {quarter}')
            try:
                file_type = file_types[0]
                with open(os.path.join(curr_dir,folder,stock,'master_reports',f'master_reports_{file_type}_{year}_{quarter}.json')) as f:
                    master_reports = json.load(f)
            except FileNotFoundError:
                file_type = file_types[1]
                try:
                    with open(os.path.join(curr_dir,folder,stock,'master_reports',f'master_reports_{file_type}_{year}_{quarter}.json')) as f:
                        master_reports = json.load(f)
                except FileNotFoundError:
                    continue


            missing_data = [item for item in financial_statements_mapping]
            # THIS NEEDS TO BE DONE WITH RE ### this text may change slightly per quarter
            statements_url = []
            dict_url = {}
            for report_dict in master_reports:
                
                report_list = financial_statements_mapping 
                for item in report_list:
                    if report_dict['name_short'].upper() in financial_statements_mapping[item]:                        

                        print('-'*100)
                        print(report_dict['name_short'])
                        print(report_dict['url'])
                        
                        try:
                            missing_data.remove(item)
                            statements_url.append(report_dict['url'])
                            dict_url[item] = report_dict['url']
                        except ValueError:
                            print(f'MULTIPLE REPORTS FOUND FOR: {item}')
            
            with open(os.path.join(curr_dir,folder,stock,'financial_statements_url',f'url{file_type}_{year}_{quarter}.json'), 'w') as f:
                json.dump(dict_url,f)
                
            if len(missing_data) != 0:
                num_missing += len(missing_data)
                missing_data_ls.append(f'Missing Data for {stock}, {year}, {quarter}, {file_type} \n {len(missing_data)}, {missing_data}')
                
            statements_data = []

            # loop through each statement url
            for statement in dict_url.values():

                # define a dictionary that will store the different parts of the statement.
                statement_data = {}
                statement_data['headers'] = []
                statement_data['sections'] = []
                statement_data['data'] = []
                
                # request the statement file content
                content = requests.get(statement, headers=SEC_headers).content
                report_soup = BeautifulSoup(content, 'lxml')

                # find all the rows, figure out what type of row it is, parse the elements, and store in the statement file list.
                for index, row in enumerate(report_soup.table.find_all('tr')):
                    
                    # first let's get all the elements.
                    cols = row.find_all('td')
                    
                    # if it's a regular row and not a section or a table header
                    if (len(row.find_all('th')) == 0 and len(row.find_all('strong')) == 0): 
                        reg_row = [ele.text.strip() for ele in cols]
                        statement_data['data'].append(reg_row)
                        
                    # if it's a regular row and a section but not a table header
                    elif (len(row.find_all('th')) == 0 and len(row.find_all('strong')) != 0):
                        sec_row = cols[0].text.strip()
                        statement_data['sections'].append(sec_row)
                        
                    # finally if it's not any of those it must be a header
                    elif (len(row.find_all('th')) != 0):            
                        hed_row = [ele.text.strip() for ele in row.find_all('th')]
                        statement_data['headers'].append(hed_row)
                        
                    else:            
                        print('We encountered an error.')

                # append it to the master list.
                statements_data.append(statement_data)
            with open(os.path.join(curr_dir,folder,stock,'financial_statements_raw',f'raw{file_type}_{year}_{quarter}.json'), 'w') as f:
                json.dump(statements_data,f)
for x in missing_data_ls:
    print(x)
    
print(f'Total: {num_missing}')
