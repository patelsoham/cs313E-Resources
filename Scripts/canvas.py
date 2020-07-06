from dotenv import load_dotenv
load_dotenv()

import os
import json
import requests
import datetime

import assignment_grader as ag
import zybooks_grader as zg

#For get/post requests to canvas API
canvas_key = os.getenv('CANVAS_KEY')
canvas_endpoint = os.getenv('CANVAS_ENDPOINT')
headers = {'authorization': 'Bearer {}'.format(canvas_key), 'content-type': 'application/json'}

student_info = {}
assignment_info = {}
folder_info = {}

#formats assignment due dates into datetime objects. TODO: format into local time rather than UTC
dt_frmt = lambda submit_time: datetime.datetime.strptime(submit_time,'%Y-%m-%dT%H:%M:%SZ')

#Get assignment names, canvas ids, and due dates
def get_assignments():
    response = requests.get(canvas_endpoint + '/assignments?per_page=50', headers=headers).json()
    for assignment in response:
        #TODO: determine a better condition to only include reading and programming assignments
        if str(assignment['name'])[0] == 'R' or str(assignment['name'])[0] == 'A':
            assignment_info.update({str(assignment['name']): [str(assignment['id']), dt_frmt(str(assignment['due_at']))]})
            print('Assignment - ' + str(assignment['name']) + ': ' + str(assignment['id']) + ', ' + str(dt_frmt(str(assignment['due_at']))))

#Get student eids and canvas id as key value pairs.
def get_students():
    response = requests.get(canvas_endpoint + '/students', headers=headers).json()
    for student in response:
        #sis_user_id == eid
        student_info.update({str(student['sis_user_id']).lower() : str(student['id']).lower()})
        #print(str(student['sis_user_id']).lower() + ' ' + str(student['id']).lower())

def get_folders():
    response = requests.get(canvas_endpoint + '/folders?per_page=50', headers=headers).json()
    for folder in response:
        if 'a' in folder['name']:
            folder_info.update({str(folder['name']): str(folder['id'])})
            print(str(folder['name']) + ' : ' +  str(folder['id']))

#updates reading assignments in the gradebook
def update_readings():
    re_grades = zg.get_readings()
    data = [{'grade_data': {}}, {'grade_data': {}}, {'grade_data': {}}, {'grade_data': {}}, {'grade_data': {}}]
    failed_eids = set()
    responses = []
    print(len(data))
    for i in range(len(data)): 
        for student in re_grades:
            try:
                data[i]['grade_data'].update({student_info[student.lower()]: {'posted_grade': re_grades[student][i]}})
            except Exception as e:
                failed_eids.add(student)
        responses.append(requests.post(canvas_endpoint + '/assignments/' + assignment_info['RE' + str(i+1)][0] + '/submissions/update_grades', headers=headers, json=(data[i])))
    #Testing purposes (determine if requests was successful and which eids failed)
    print(str(responses) + '\n' + str(failed_eids))
    pass

#updates programming assignments in gradebook.
def update_assignments():
    hackerrank_grades = ag.get_submissions()
    failed_eids = set()
    data = [{'grade_data': {}}, {'grade_data': {}}, {'grade_data': {}}]
    responses = []
    for i in range(len(data)):
        print('__________________________________________' +'A' + str(i+1)+ '__________________________________________')
        for entry in hackerrank_grades['A' + str(i+1)]:
            try:
                print('Unupdated Score: ' + str(entry.eid) + ' ' + str(entry.score) + ' ' + str(entry.submit_time) + ' ' + str(assignment_info['A' + str(i+1)][1]))
                entry.update_score(assignment_info['A' + str(i+1)][1])
                print('Updated Score: ' + str(entry.eid) + ' ' + str(entry.score) + ' ' + str(entry.pdf) + '\n\n')
                data[i]['grade_data'].update({student_info[entry.eid.lower()]: {'posted_grade': entry.get_score()}})
            except Exception as err:
                failed_eids.add(entry.eid)
                print(err)
        #responses.append(requests.post(canvas_endpoint + '/assignments/' + assignment_info['A' + str(i+1)][0] + '/submissions/update_grades', headers=headers, json=(data[i])))
    #Testing purposes (determine if requests was successful and which eids failed)
    print(str(responses) + '\n' + str(failed_eids))
    return None

    def upload_files():
        get_folders()

if __name__ == '__main__':
    
    get_students()
    get_assignments()
    update_readings()
    #update_assignments()
    
    