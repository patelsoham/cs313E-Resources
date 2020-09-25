from dotenv import load_dotenv
load_dotenv()

import os
import pandas as pd
import datetime as dt

#generates dictionary from numpy array with eid and list of reading assignment grades as key value pairs
gen_dict = lambda arr: {row[0]: row[1:].tolist() for row in arr}
get_score = lambda name: name[name.index('(') + 1: name.index(')')]

#TODO: automate csv download from zybooks (requests/selenium)

#Checks if updated csv has been downloaded.
#Multiple csvs return a list instead
def get_csv_path():
    csvs = os.listdir(os.getenv('SCRIPT_PATH') + '/static_data/csvs')
    results = []
    for csv in csvs:
        if str(dt.date.today()) in csv:
            results.append(os.getenv('SCRIPT_PATH') + '/static_data/csvs/' + csv)
    return results if len(results) > 0 else "Download from zybooks not found in folder"
    

#Return dataframe containing eids and reading assignment grades
def get_readings():
    csvs = get_csv_path()
    results = {}
    for csv in csvs:
        try:
            dataset = pd.read_csv(csv)
            dataset = dataset.drop([col for col in list(dataset) if col != 'Student ID' and 'E' not in col], axis=1)
            for col in dataset:
                if col != 'Student ID':
                    dataset[col] = (dataset[col] /100) * int(get_score(col))
            results.update(gen_dict(dataset.to_numpy()))
        except Exception as e:
            print(str(csv) + '\n' + str(e))
            return None
    return results

if __name__ == '__main__':
    result = get_readings()
    print(result)