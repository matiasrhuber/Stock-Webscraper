import pandas as pd
import os
import yaml
import json
from IPython.display import display

### PARAMETERS ###
with open("SEC_config.yaml") as f:
    cfg = yaml.load(f)

years = range(cfg['years']['start'],cfg['years']['end'])
stocks = cfg['stocks']
period_mapping = {'_10-q' : '3 Months Ended', '_10-k' : '12 Months Ended'}
financial_statements_mapping = cfg['financial_statements_mapping']
curr_dir = os.getcwd()
folder = 'SEC'
############################################

def get_key(val):
   
    for key, value in financial_statements_mapping.items():
        if val == value:
            return key
 
    return "key doesn't exist"

# Grab the proper components
error_ls = []
### Figure out all possible formatting according to document title, number of headers, and display table accordingly ###

for stock in stocks:
    try:
        os.mkdir(os.path.join(curr_dir,folder,stock,'tabular_data'))
    except:
        pass
    data_dir = os.path.join(curr_dir,folder,stock,'financial_statements_raw')
    for data in os.listdir(data_dir):
        with open(os.path.join(data_dir,data)) as f:
            statements_data = json.load(f)
        
        file_name = data.replace('.json','').replace('raw','')
        file_type = file_name[0:5]
        file_year = file_name[6:10]
        file_quarter = file_name[11:15]

        if int(file_year) not in years:
            print(f'skipping {data}')
            continue
        else:
            print(f'running {data}')
        for i in range(4):
            header_title = statements_data[i]['headers'][0][0].split(' - USD')[0]
            file_title = header_title#[k for k,v in financial_statements_mapping.items() if v == header_title] #get_key(header_title)

            if len(statements_data[i]['headers']) != 1:
                subheaders = statements_data[i]['headers'][1]
                overheaders = statements_data[i]['headers'][0][1:]
                mult = int(len(subheaders)/len(overheaders))
                overheaders_table = [item for item in overheaders for _ in range(mult)]
                income_header = [x+' ('+y+')' for x,y in zip(subheaders,overheaders_table)]
            else:
                subheaders = statements_data[i]['headers'][0][1:]
                income_header = [x+' ('+period_mapping[file_type]+')' for x in subheaders]

            # income_header =  statements_data[i]['headers'][-1] #threee months ended gives different formatting #[0][1:]
            income_data = statements_data[i]['data']


            # Put the data in a DataFrame
            income_df = pd.DataFrame(income_data)

            # Define the Index column, rename it, and we need to make sure to drop the old column once we reindex.
            income_df.index = income_df[0]
            income_df.index.name = 'Category'
            income_df = income_df.drop(0, axis = 1)

            # Get rid of the '$', '(', ')', and convert the '' to NaNs.
            income_df = income_df.replace('[\$,)]','', regex=True )\
                                .replace( '[(]','-', regex=True)\
                                .replace( '', 'NaN', regex=True)


            # everything is a string, so let's convert all the data to a float.

            income_df = income_df.astype(float, errors='ignore')

            
            # Change the column headers
            try:
                income_df.columns = income_header
            except:
                display(income_df)
                error_ls.append(stock+data)
                continue

            current_dir = os.getcwd()
            try:
                folder_dir = os.path.join(current_dir,'SEC',stock)
                os.mkdir(folder_dir)
            except:
                print(f'Saving over data for {stock} in {file_year} {file_quarter}...')
            income_df.to_csv(os.path.join(folder_dir,'tabular_data',f"{file_title+file_year+file_quarter+file_type}.csv"))

print(error_ls)
print(f'Data Unable to save in tabular form: {len(error_ls)}')