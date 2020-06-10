from dotenv import load_dotenv
load_dotenv()

import os
import sys
sys.path.insert(1, os.getenv('SOL_PATH'))

import A1_Spiral as a1
import A2_Cipher as a2
import random as rand

# NOTE: Problem refers to HackerRank Problem for the Assignment Submissions 
# (i.e. Assignment 1 contained two HackerRank problems in its test: create_spiral and sum_sub_grid)

#converts testcase number to proper string for HackerRank input/output files (i.e. 0 -> 00, 1 -> 01, etc)
format_str = lambda i, num_tests: ('0' * ((len(num_tests)-len(i)) if (len(num_tests)-len(i)) >= 2 else 1)) + i
#generates file path depending on problem, input/output, and number
file_name = lambda problem, stem, num: problem + ('/input' if stem == 0 else '/output') + num + '.txt'

#For input/output.txt file paths
script_dir = os.getenv('SCRIPT_PATH')
#Dictionary with each key(problem) having an array of file path tuples for each test case
file_paths = {'a1/create_spiral': [], 'a1/sum_sub_grid': [], 'a2/encrypt': [], 'a2/decrypt': []}

#Gets the file_paths
def init_paths(num_tests):
    #populates proper file names given the number of test cases into file_paths
    testcase_nums = [format_str(str(i), str(num_tests)) for i in range(num_tests)]
    for num in testcase_nums:
        for func in file_paths:
            #tuple that holds input file and output file paths
            temp = (file_name(func, 0, num), file_name(func, 1, num))
            file_paths[func].append(temp)
    return None

def a1_test_cases():
    #Choose correct file paths for assignment 1's problem
    assign_num = a1_test_cases.__name__[0:2]
    for problem in file_paths:
        if assign_num in problem:
            for testcase in file_paths[problem]:
                input_path = os.path.join(script_dir, testcase[0])
                output_path = os.path.join(script_dir, testcase[1])
    return None

def a2_test_cases():
    #Choose correct file paths for assignment 2's problems
    assign_num = a2_test_cases.__name__[0:2]
    for problem in file_paths:
        if assign_num in problem:
            for testcase in file_paths[problem]:
                input_path = os.path.join(script_dir, testcase[0])
                output_path = os.path.join(script_dir, testcase[1])
    return None

def main():
    n = int(input('Number of test cases generated: '))
    init_paths(n)
    a1_test_cases()
    return None

if __name__ == '__main__':
    main()
