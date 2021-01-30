from dotenv import load_dotenv
load_dotenv()

import os
import json
import requests
import datetime
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

import assignment_grader as ag
import zybooks_grader as zg

#For get/post requests to canvas API
canvas_key = os.getenv('CANVAS_KEY')
canvas_endpoint = os.getenv('CANVAS_ENDPOINT')
headers = {'authorization': 'Bearer {}'.format(canvas_key), 'content-type': 'application/json'}

assignment_info = {}
folder_info = {}

#formats assignment due dates into datetime objects. TODO: format into local time rather than UTC
dt_frmt = lambda submit_time: datetime.datetime.strptime(submit_time,'%Y-%m-%dT%H:%M:%SZ')
update_dict = lambda sis_user_id, canvas_id, reverse: {str(canvas_id).lower(): [str(sis_user_id).lower(), 0]} if reverse else {str(sis_user_id).lower(): [str(canvas_id).lower(), 0]}

#Get assignment names, canvas ids, and due dates
def get_assignments(reading_assigns = [], prog_assigns = [], exams = []):
    response = requests.get(canvas_endpoint + '/assignments?per_page=100', headers=headers).json()
    for assignment in response:
        #TODO: determine a better condition to only include reading and programming assignments
        #print(assignment['name'])
        if str(assignment['name']).lower() in reading_assigns or str(assignment['name']).lower() in prog_assigns or str(assignment['name']).lower() in exams:
            if str(assignment['name']).lower() in ['a6', 'a7', 'a8']:
                assignment_info.update({str(assignment['name']): [str(assignment['id']), dt_frmt('2020-10-30T04:59:59Z')]})
            else:
                assignment_info.update({str(assignment['name']): [str(assignment['id']), dt_frmt(str(assignment['due_at']))]})
            print('Assignment - ' + str(assignment['name']) + ': ' + str(assignment['id']) + ', ' + str(assignment_info[str(assignment['name'])][1]))
    return assignment_info

#Get student eids and canvas id as key value pairs.
def get_students(reverse = False):
    student_info = {}
    response = requests.get(canvas_endpoint + '/students', headers=headers).json()
    for student in response:
        #sis_user_id == eid
        student_info.update(update_dict(student['sis_user_id'], student['id'], reverse))
        #print(str(student['sis_user_id']).lower() + ' ' + str(student['id']).lower())
    return student_info

def get_folders():
    response = requests.get(canvas_endpoint + '/folders?per_page=50', headers=headers).json()
    for folder in response:
        if 'a' in folder['name']:
            folder_info.update({str(folder['name']): str(folder['id'])})
            print(str(folder['name']) + ' : ' +  str(folder['id']))

#updates reading assignments in the gradebook
def update_readings(readings):
    student_info = get_students()
    re_grades = zg.get_readings()
    data = {}
    for i in readings:
        data.update({i : {'grade_data': {}}})
    failed_eids = set()
    responses = []
    fptr = open('static_data/zybooks.txt', 'w')
    for name in readings: 
        for student in re_grades:
            try:
                print(f'{student}: {re_grades[student][int(name[1:]) - 1]}')
                data[name]['grade_data'].update({student_info[student.lower()][0]: {'posted_grade': re_grades[student][int(name[1:]) - 1]}})
            except Exception as e:
                print(e)
                failed_eids.add(student)
        responses.append(requests.post(canvas_endpoint + '/assignments/' + assignment_info[name.upper()][0] + '/submissions/update_grades', headers=headers, json=(data[name])))
        #Testing purposes (determine if requests was successful and which eids failed)
        fptr.write(str('\n____________________________________________________________________________________' + name.upper() +  '____________________________________________________________________________________' + '\n'))
        fptr.write(str(responses) + '\n'  + str(len(failed_eids)) + '\n')
        for id in failed_eids:
            fptr.write(f'{id}: ')
            for name in readings:
                fptr.write(f'({name} - {re_grades[student][int(name[1:]) - 1]}), ')
            fptr.write('\n')
    fptr.close()

#updates programming assignments in gradebook.
def update_assignments():
    get_students()
    hackerrank_grades = ag.get_submissions([key[1:] for key in assignment_info.keys() if key[0] == 'A'], False)
    failed_eids = set()
    data = {}
    responses = []
    fptr = open('static_data/canvas.txt', 'w')
    for assignment in hackerrank_grades:
        fptr.write('__________________________________________' + assignment + '__________________________________________\n')
        data.update({assignment: {'grade_data': {}}})
        for entry in hackerrank_grades[assignment]:
            try:
                #Update Score Based on when late penalties
                fptr.write('Unupdated Score: ' + str(entry.eid) + ' ' + str(entry.score) + ' ' + str(entry.submit_time) + ' ' + str(assignment_info[assignment][1]) + '\n')
                entry.update_score(assignment_info[assignment][1])
                fptr.write('Updated Score: ' + str(entry.eid) + ' ' + str(entry.score) + ' ' + str(entry.pdf) + '\n\n')
                data[assignment]['grade_data'].update({student_info[entry.eid.lower()]: {'posted_grade': entry.get_score()}})
                if entry.partner_eid != None:
                    #add in partner submission after grade adjustments
                    data[assignment]['grade_data'].update({student_info[entry.partner_eid.lower()]: {'posted_grade': entry.get_score()}})
            except Exception as err:
                failed_eids.add(entry.eid)
                fptr.write('Err is ' + str(err) + '\n')
        responses.append(requests.post(canvas_endpoint + '/assignments/' + assignment_info[assignment][0] + '/submissions/update_grades', headers=headers, json=(data[assignment])))
        #Debugging output
        fptr.write('Debugging output ' + str(responses) + '\n' + str(failed_eids) + '\n' + str(len(failed_eids)) + ' ' + str(len(student_info)) + '\n')
    return None

def get_test_csv(csv):
    cols = [col for col in list(pd.read_csv(csv, nrows = 1)) if col == 'Eid' or 'Question ' in col]
    dataset = pd.read_csv(csv, usecols=cols)
    dataset = dataset.drop('Question 1', axis=1)
    dataset.insert(len(dataset.columns), 'Test 2', 0, True)
    for i in range(len(dataset)):
        question_scores = [int(dataset[dataset.columns[n]][i]) for n in range(1,len(dataset.columns) - 1)]
        dataset['Test 2'][i] = sum(question_scores) - min(question_scores[:-1])
    freq_distribution = dataset['Test 2'].value_counts().to_dict()
    plt.bar(list(freq_distribution.keys()), list(freq_distribution.values()))
    plt.xlabel('Test Scores')
    plt.ylabel('# of Students')
    plt.title('Score Distributions')
    plt.show()
    scores = np.array(dataset['Test 2'].tolist())
    print(f'Average: {np.average(scores)}')
    print(f'Median: {np.median(scores)}')
    print(f'Std Dev: {np.std(scores)}') 
    dataset.to_csv('test_2_grades.csv')

if __name__ == '__main__':
    prog_assignments = set(input('Enter which programming assignments are being graded: ').split())
    reading_assignments = set(input('Enter which reading assignments are being graded: ').split())
    get_assignments(prog_assignments, reading_assignments, [])
    update_readings(reading_assignments)
    
    