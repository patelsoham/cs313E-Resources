from dotenv import load_dotenv
load_dotenv()

import os
import re
import sys

sys.path.insert(1, os.getenv('SOL_PATH'))
script_dir = os.getenv('SCRIPT_PATH')

import a6_submissions as a6_sub
import a7_submissions as a7_sub
import importlib

get_module = lambda module_name, module_path: importlib.util.module_from_spec(importlib.util.spec_from_file_location(module_name, module_path, submodule_search_locations=[]))


#each file renamed
def rename_submissions(assign_no, sub_dir):
    for file_name in os.listdir(sub_dir):
        if '__' not in file_name:
            ind = file_name.rfind('_')
            os.rename(sub_dir + file_name, f'{sub_dir}{file_name[:ind]}_a{assign_no}.py')
    return sub_dir

def get_modules():
    modules = []
    for submission in a6_sub.modules:
        modules.append(importlib.import_module('.' + submission[submission.rfind('/') + 1:-3], a6_sub.__name__))
    return modules

def prep_submissions(assign_no):
    sub_dir = os.listdir()[os.listdir().index(f'a{assign_no}_submissions')] + '/'
    sub_dir = rename_submissions(assign_no, sub_dir)
    for file_name in os.listdir(sub_dir):
        if '__' not in file_name:
            mod_submissions(sub_dir + file_name)
    modules = get_modules()

def mod_submissions(file_path):
    try:
        fptr = open(file_path, 'r+')
        lines = fptr.read()
        if 'if __name__ == \'__main__\':\n\tmain()' in lines:
            #print(f'{file_path}: they have __name__ == __main__')
        else:
            #print(f'{file_path}: they do not have __name__ == __main__')
            lines = re.sub('^main\(\)$', 'if __name__ == \'__main__\':\n\tmain()', lines, flags=re.MULTILINE)
            fptr.seek(0)
            fptr.write(lines)
    except:
        print(file_path)

prep_submissions(6)
# test_mod = importlib.import_module('.nguyenjason_LATE_4289130_56460727_a6', 'a6_submissions')
# print(dir(test_mod))
