from dotenv import load_dotenv
load_dotenv()

import os
import sys
sys.path.insert(1, os.getenv('SOL_PATH'))

import A1_Spiral as a1
import A2_Cipher as a2
import random as rand

#For input/output.txt file paths
script_dir = os.getenv('SCRIPT_PATH')
a1_paths = {'create_spiral': [], 'sum_sub_grid': []}
a2_paths = {'encrypt': [], 'decrypt': []}

def a1_test_cases():
    pass

def a2_test_cases():
    pass

def main():


    pass

if __name__ == '__main__':
    main()
