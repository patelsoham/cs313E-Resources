from dotenv import load_dotenv
load_dotenv()

import os
import sys
sys.path.insert(1, os.getenv('SOL_PATH'))

#Assignment Imports
import A1_Spiral as a1
import A2_Cipher as a2


#Additional Packages
import math
import json
import requests
import random as rand


# NOTE: Problem refers to HackerRank Problem for the Assignment Submissions 
# (i.e. Assignment 1 contained two HackerRank problems in its test: create_spiral and sum_sub_grid)

#converts testcase number to proper string for HackerRank input/output files (i.e. 0 -> 00, 1 -> 01, etc)
format_str = lambda i, num_tests: ('0' * ((len(num_tests)-len(i)) if (len(num_tests)-len(i)) >= 2 else 1)) + i
#generates file path depending on problem, input/output, and number
file_name = lambda problem, stem, num: problem + ('/input' if stem == 0 else '/output') + num + '.txt'
#Determines which problems' testcases we are currently generating
choose_func = lambda func_name, input_path, output_path: (func_name in input_path and func_name in output_path) 

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

#Generates Assignment 1's testcases
def a1_test_cases():
    #Choose correct file paths for assignment 1's problem
    assign_num = a1_test_cases.__name__[0:2]
    for problem in file_paths:
        if assign_num in problem:
            for testcase in file_paths[problem]:
                input_path = os.path.join(script_dir, testcase[0])
                output_path = os.path.join(script_dir, testcase[1])
                #Determine which problems' testcases are being generated based on file path
                if choose_func(a1.create_spiral.__name__, input_path, output_path):
                    #create_spiral's test cases
                    dim = rand.randint(5, 100)
                    #Write input values
                    fptr = open(input_path, 'w')
                    fptr.write(str(dim))
                    fptr.close()
                    #write output
                    fptr = open(output_path, 'w')
                    try: 
                        write_arr(fptr, a1.create_spiral(dim))
                    except Exception as e: 
                        print(a1.create_spiral.__name__ + ' failed (dim): ' + str(dim))
                        print(e)
                    finally:
                        fptr.close()
                elif choose_func(a1.sum_sub_grid.__name__, input_path, output_path):
                    #sum_sub_grid's test cases
                    dim = rand.randint(5, 100)
                    val = rand.randint(1, math.ceil(pow(dim, 2)*1.5))
                    #write input values
                    fptr = open(input_path, 'w')
                    fptr.write(str(dim) + str(val))
                    fptr.close()
                    #write output
                    fptr = open(output_path, 'w')
                    try:
                        fptr.write(str(a1.sum_sub_grid(a1.create_spiral(dim), val)))
                    except Exception as e:
                        print(a1.sum_sub_grid.__name__ + ' failed (dim, val): ' + '(' + str(dim) + ', ' + str(val) + ') ' + testcase[1])
                        print(e)
                    finally:
                        fptr.close()
                else:
                    print('Either file path incorrect: ' + '\n' + 'Input Path: ' + input_path + 'Output Path: ' + output_path)
    return None

#Generates Assignment 2's testcases
def a2_test_cases():
    words = requests.get("http://raw.githubusercontent.com/sindresorhus/mnemonic-words/master/words.json").json()
    #Choose correct file paths for assignment 2's problems
    assign_num = a2_test_cases.__name__[0:2]
    for problem in file_paths:
        if assign_num in problem:
            for testcase in file_paths[problem]:
                input_path = os.path.join(script_dir, testcase[0])
                output_path = os.path.join(script_dir, testcase[1])
                phrase = rand.choice(words)
                fptr = open(input_path, 'w')
                fptr.write(str(phrase))
                fptr.close()
                fptr = open(output_path, 'w')
                try:
                    #Determine which problems' testcases are being generated based on file path
                    if choose_func(a2.encrypt.__name__, input_path, output_path):
                        fptr.write(a2.encrypt(phrase))
                    elif choose_func(a2.decrypt.__name__, input_path, output_path):
                        fptr.write(a2.decrypt(phrase))
                    else:
                        print('Either file path incorrect: ' + '\n' + 'Input Path: ' + input_path + 'Output Path: ' + output_path)
                except Exception as e:
                    if choose_func(a2.encrypt.__name__, input_path, output_path):
                        print(a2.encrypt.__name__ + ' failed (phrase): ' + phrase)
                    elif choose_func(a2.decrypt.__name__, input_path, output_path):
                        print(a2.decrypt.__name__ + ' failed (phrase): ' + phrase)
                    print(e)
                finally:
                    fptr.close()
    return None



#writes array in formatted manner
def write_arr (fptr, temp):
    mx = max((len(str(ele)) for sub in temp for ele in sub))
    for row in temp:
        fptr.write(" ".join(["{:<{mx}}".format(ele,mx=mx) for ele in row]) + '\n')

def main():
    n = int(input('Number of test cases generated: '))
    init_paths(n)
    a1_test_cases()
    a2_test_cases()
    return None

if __name__ == '__main__':
    main()
