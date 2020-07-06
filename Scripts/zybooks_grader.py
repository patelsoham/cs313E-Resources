from dotenv import load_dotenv
load_dotenv()

import os
import pandas as pd
import datetime as dt

#generates dictionary from numpy array with eid and list of reading assignment grades as key value pairs
gen_dict = lambda arr: {row[0]: row[1:].tolist() for row in arr}

#TODO: automate csv download from zybooks (requests/selenium)

#Checks if updated csv has been downloaded.
def get_csv_path():
    csvs = os.listdir(os.getenv('SCRIPT_PATH') + '/static_data/csvs')
    for csv in csvs:
        if str(dt.date.today()) in csv:
            return os.getenv('SCRIPT_PATH') + '/static_data/csvs/' + csv
    return 'Download not found, please redownload csv from zybooks'

#Return dataframe containing eids and reading assignment grades
def get_readings():
    csv = get_csv_path()
    try:
        dataset = pd.read_csv(csv)
        dataset = dataset.drop([col for col in list(dataset) if col != 'Student ID' and not 'RE' in col], axis=1)
        for col in dataset:
            if col != 'Student ID':
                dataset[col] = (dataset[col] /100) * int(col[5:8])
        return gen_dict(dataset.to_numpy())
    except Exception as e:
        print(str(csv) + '\n' + str(e))
        return None

if __name__ == '__main__':
    result = get_readings()
    #print(result)