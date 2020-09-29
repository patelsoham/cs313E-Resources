from dotenv import load_dotenv
load_dotenv()

import os
import sys
import shutil
sys.path.insert(1, os.getenv('SOL_PATH'))

#Assignment Imports
import A1_Spiral as a1
import A2_Cipher as a2
import A3_Intervals as a3
import A6_ConvexHull as a6
import A7_Work as a7
import A8_PathSum as a8
import A9_Boxes as a9
import A10_MaxPath as a10
import A13_Josephus as a13


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
file_paths = {'static_data/a1/create_spiral': [], 'static_data/a1/sum_sub_grid': [], 'static_data/a2/encrypt': [], 'static_data/a2/decrypt': [], 'static_data/a3/merge_tuples': [], 'static_data/a3/sort_by_interval_size': [], \
              'static_data/a6/convex_hull': [], 'static_data/a6/area_poly': [], 'static_data/a7/linear_search': [], 'static_data/a7/binary_search': [], 'static_data/a8/count_paths': [], 'static_data/a8/path_sum': [], \
              'static_data/a9/gen_all_boxes': [], 'static_data/a9/largest_nesting_subsets': [], 'static_data/a10/greedy': [], 'static_data/a10/other_methods': [], 'static_data/a13/josephus': []}

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
                        print(a1.create_spiral.__name__ + ' failed (dim): ' + str(dim) + '\n' + e)
                    finally:
                        fptr.close()
                elif choose_func(a1.sum_sub_grid.__name__, input_path, output_path):
                    #sum_sub_grid's test cases
                    dim = rand.randint(5, 100)
                    val = rand.randint(1, math.ceil(pow(dim, 2)*1.5))
                    #write input values
                    fptr = open(input_path, 'w')
                    fptr.write(str(dim) + ' ' + str(val))
                    fptr.close()
                    #write output
                    fptr = open(output_path, 'w')
                    try:
                        fptr.write(str(a1.sum_sub_grid(a1.create_spiral(dim), val)))
                    except Exception as e:
                        print(a1.sum_sub_grid.__name__ + ' failed (dim, val): ' + '(' + str(dim) + ', ' + str(val) + ') ' + testcase[1] + '\n' + e)
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
                        print(a2.encrypt.__name__ + ' failed (phrase): ' + phrase + '\n' + e)
                    elif choose_func(a2.decrypt.__name__, input_path, output_path):
                        print(a2.decrypt.__name__ + ' failed (phrase): ' + phrase + '\n' + e)
                    print(e)
                finally:
                    fptr.close()
    return None

def a3_test_cases():
     #Choose correct file paths for assignment 3's problem
    assign_num = a3_test_cases.__name__[0:2]
    for problem in file_paths:
        if assign_num in problem:
            for testcase in file_paths[problem]:
                input_path = os.path.join(script_dir, testcase[0])
                output_path = os.path.join(script_dir, testcase[1])
                #generates a random number of intervals
                intervals = a3.gen_intervals(rand.randint(5, 25))
                fptr = open(input_path, 'w')
                fptr.write(str(len(intervals)) + '\n')
                for interval in intervals:
                    fptr.write(str(interval[0]) + ' ' + str(interval[1]) + '\n')
                fptr.close()
                fptr = open(output_path, 'w')
                try:
                    #Determine which problems' testcases are being generated by file path
                    if choose_func(a3.merge_tuples.__name__, input_path, output_path):
                        result = a3.merge_tuples(intervals)
                        for res in result:
                            fptr.write(str(res[0]) + ' ' + str(res[1]) + '\n')
                    elif choose_func(a3.sort_by_interval_size.__name__, input_path, output_path):
                        result = a3.sort_by_interval_size(a3.merge_tuples(intervals))
                        for res in result:
                            fptr.write(str(res[0]) + ' ' + str(res[1]) + '\n')
                    else:
                        print('Either file path incorrect: ' + '\n' + 'Input Path: ' + input_path + 'Output Path: ' + output_path)
                except Exception as e:
                    if choose_func(a3.merge_tuples.__name__, input_path, output_path):
                        print(a3.merge_tuples.__name__ + ' failed on ' + input_path[-11:] + '\n' + e)
                    elif choose_func(a3.sort_by_interval_size.__name__, input_path, output_path):
                        print(a3.sort_by_interval.__name__ + ' failed on ' + input_path[-11:] + '\n' + e)
                finally:
                    fptr.close()         
    return None

def a6_test_cases():
    assign_num  = a6_test_cases.__name__[0:2]
    for problem in file_paths:
        if assign_num in problem:
            for testcase in file_paths[problem]:
                input_path = os.path.join(script_dir, testcase[0])
                output_path = os.path.join(script_dir, testcase[1])
                points = a6.gen_points(rand.randint(3, 101))
                fptr = open(input_path, 'w')
                fptr.write(str(len(points)) + '\n')
                for point in points:
                    fptr.write(str(point.x) + ' ' + str(point.y) + '\n')
                fptr.close()
                fptr = open(output_path, 'w')
                try:
                    #Determine which problems' testscases are being generated by file path
                    if choose_func(a6.convex_hull.__name__, input_path, output_path):
                        points.sort(key=a6.sort_points)
                        result = a6.convex_hull(points)
                        for point in result:
                            fptr.write(str(point.x) + ' ' + str(point.y) + '\n')
                    elif choose_func(a6.area_poly.__name__, input_path, output_path):
                        points.sort(key=a6.sort_points)
                        fptr.write(str(a6.area_poly(a6.convex_hull(points))))
                    else:
                        print('Either file path incorrect: ' + '\n' + 'Input Path: ' + input_path + 'Output Path: ' + output_path)
                except Exception as e:
                    if choose_func(a6.convex_hull.__name__, input_path, output_path):
                        print(a6.convex_hull.__name__ + ' failed on ' + input_path[-11:] + '\n' + str(e))
                    elif choose_func(a6.area_poly.__name__, input_path, output_path):
                        print(a6.area_poly.__name__ + ' failed on ' + input_path[-11:] + '\n' + str(e))
                finally:
                    fptr.close()
    return None

def a7_test_cases():
    assign_num = a7_test_cases.__name__[0:2]
    for problem in file_paths:
        if assign_num in problem:
            for testcase in file_paths[problem]:
                input_path = os.path.join(script_dir, testcase[0])
                output_path = os.path.join(script_dir, testcase[1])
                nums = a7.gen_input()
                fptr = open(input_path, 'w')
                fptr.write(str(nums[0]) + ' ' + str(nums[1]))
                fptr.close()
                fptr = open(output_path, 'w')
                try:
                    if choose_func(a7.linear_search.__name__, input_path, output_path) or choose_func(a7.binary_search.__name__, input_path, output_path):
                        fptr.write(str(a7.binary_search(nums[0], nums[1])))
                    else:
                        print('Either file path incorrect: ' + '\n' + 'Input Path: ' + input_path + 'Output Path: ' + output_path)
                except Exception as e:
                    if choose_func(a7.linear_search.__name__, input_path, output_path):
                        print(a7.linear_search.__name__ + ' failed on ' + input_path[-11:] + '\n' + str(e))
                    elif choose_func(a7.binary_search.__name__, input_path, output_path):
                        print(a7.binary_search.__name__ + ' failed on ' + input_path[-11:] + '\n' + str(e))
                finally:
                    fptr.close()
    return None

def a8_test_cases():
    used_dims = set()
    assign_num = a8_test_cases.__name__[0:2]
    for problem in file_paths:
        if assign_num in problem:
            for testcase in file_paths[problem]:
                input_path = os.path.join(script_dir, testcase[0])
                output_path = os.path.join(script_dir, testcase[1])
                inpt = a8.gen_input(used_dims)
                used_dims.add(inpt[0])
                fptr = open(input_path, 'w')
                fptr.write(str(inpt[0]) + '\n')
                if choose_func(a8.path_sum.__name__, input_path, output_path):
                    grid = inpt[1]
                    write_arr(fptr, grid)
                fptr.close()
                fptr = open(output_path, 'w')
                try:
                    if choose_func(a8.count_paths.__name__, input_path, output_path):
                        fptr.write(str(a8.count_paths(inpt[0])))
                    elif choose_func(a8.path_sum.__name__, input_path, output_path):
                        fptr.write(str(a8.path_sum(inpt[1], inpt[0])))
                    else:
                        print('Either file path incorrect: ' + '\n' + 'Input Path: ' + input_path + ' Output Path: ' + output_path)
                except Exception as e:
                    if choose_func(a8.count_paths.__name__, input_path, output_path):
                        print(a8.count_paths.__name__ + ' failed on ' + input_path[-11:] + '\n' + str(e))
                    elif choose_func(a8.path_sum.__name__, input_path, output_path):
                        print(a8.path_sum.__name__ + ' failed on ' + input_path[-11:] + '\n' + str(e))
                finally:
                    fptr.close()


def a9_test_cases():
    assign_num = a9_test_cases.__name__[0:2]
    for problem in file_paths:
        if assign_num in problem:
            for testcase in file_paths[problem]:
                input_path = os.path.join(script_dir, testcase[0])
                output_path = os.path.join(script_dir, testcase[1])
                fptr = open(input_path, 'w')
                inpt_boxes = a9.gen_input()
                fptr.write(str(len(inpt_boxes)) + '\n')
                for box in inpt_boxes:
                    fptr.write(str(box[0]) + ' ' + str(box[1]) + ' ' + str(box[2]) + '\n')
                    box.sort()
                inpt_boxes.sort()
                fptr.close()
                fptr = open(output_path, 'w')
                try:
                    if choose_func(a9.gen_all_boxes.__name__, input_path, output_path):
                        result = []
                        a9.gen_all_boxes(inpt_boxes, [], 0, result)
                        assert(len(result) == pow(2, len(inpt_boxes)))
                        for i in range(len(result)):
                            for j in range(len(result[i])):
                                fptr.write(str(result[i][j]) + '\n')
                            fptr.write('\n')
                    elif choose_func(a9.largest_nesting_subsets.__name__, input_path, output_path):
                        result = []
                        a9.sub_sets_boxes(inpt_boxes, [], 0, result)
                        nesting_boxes = []
                        a9.largest_nesting_subsets(result, 0, nesting_boxes)
                        for i in range(len(nesting_boxes)):
                            for j in range(len(nesting_boxes[i])):
                                fptr.write(str(nesting_boxes[i][j]) + '\n')
                            fptr.write('\n')
                    else:
                        print('Either file path incorrect: ' + '\n' + 'Input Path: ' + input_path + ' Output Path: ' + output_path)
                except Exception as e:
                    if choose_func(a9.gen_all_boxes.__name__, input_path, output_path):
                        print(a9.gen_all_boxes.__name__ + ' failed on ' + input_path[-11:] + '\n' + str(e))
                    elif choose_func(a9.largest_nesting_subsets.__name__, input_path, output_path):
                        print(a9.largest_nesting_subsets.__name__ + ' failed on ' + input_path[-11:] + '\n' + str(e))
                finally:
                    fptr.close()
    return None

def a10_test_cases():
    assign_num = a10_test_cases.__name__[0:2]
    for problem in file_paths:
        if assign_num in problem:
            for testcase in file_paths[problem]:
                input_path = os.path.join(script_dir, testcase[0])
                output_path = os.path.join(script_dir, testcase[1])
                fptr = open(input_path, 'w')
                inpt = a10.gen_input()
                fptr.write(str(len(inpt)) + '\n')
                for row in inpt:
                    for num in row:
                        fptr.write(str(num) + ' ')
                    fptr.write('\n')
                fptr.close()
                fptr = open(output_path, 'w')
                try:
                    if choose_func(a10.greedy.__name__, input_path, output_path):
                        fptr.write(str(a10.greedy(inpt)))
                    else:
                        fptr.write(str(a10.dynamic_prog(inpt)))
                except Exception as e:
                    if choose_func(a10.greedy.__name__, input_path, output_path):
                        print(a10.greedy.__name__ + ' failed on ' + input_path[-11:] + '\n' + str(e))
                    else:
                        print('Other methods failed on ' + input_path[-11:] + '\n' + str(e))
                finally:
                    fptr.close()
    return None

def a13_test_cases():
    assign_num = a13_test_cases.__name__[0:2]
    for problem in file_paths:
        if assign_num in problem:
            for testcase in file_paths[problem]:
                input_path = os.path.join(script_dir, testcase[0])
                output_path = os.path.join(script_dir, testcase[1])
                fptr = open(input_path, 'w')
                inpt = a13.gen_input()
                for num in inpt:
                    fptr.write(str(num) + '\n')
                fptr = open(output_path, 'w')
                try:
                    if choose_func(a13.josephus.__name__, input_path, output_path):
                        output = a13.josephus(inpt[0], inpt[1], inpt[2])
                        for num in output:
                            fptr.write(str(num) + ' ')
                    else:
                        print('Either file path incorrect: ' + '\n' + 'Input Path: ' + input_path + ' Output Path: ' + output_path)
                except Exception as e:
                    if choose_func(a13.josephus.__name__, input_path, output_path):
                        print(a13.josephus.__name__ + ' failed on ' + input_path[-11:] + '\n' + str(e))
                    else:
                        print('Unknown Bug for  ' + input_path[-11:] + '\n' + str(e))
                finally:
                    fptr.close()
    return None
#writes array in formatted manner
def write_arr (fptr, temp):
    mx = max((len(str(ele)) for sub in temp for ele in sub))
    for row in temp:
        fptr.write(" ".join(["{:<{mx}}".format(ele,mx=mx) for ele in row]) + '\n')

#Zip testcases for each assignment into corresponding zip files
def zip_test_cases():
    for path in file_paths:
        if len(file_paths[path]) != 0:
            try:
                dir_path = os.path.join(script_dir, path)
                shutil.make_archive(dir_path.rsplit('/', 1)[1] + '_testcases','zip', dir_path)
                shutil.move(dir_path.rsplit('/', 1)[1] + '_testcases.zip', os.path.join(script_dir, 'static_data/test_case_zips'))
            except Exception as e:
                os.remove(dir_path.rsplit('/', 1)[1] + '_testcases.zip')
                print(e)

def main():
    init_paths(int(input('Number of test cases generated: ')))
    a1_test_cases()
    a2_test_cases()
    a3_test_cases()
    a6_test_cases()
    a7_test_cases()
    a8_test_cases()
    a9_test_cases()
    a10_test_cases()
    a13_test_cases()
    zip_test_cases()
    return None

if __name__ == '__main__':
    main()
