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
def get_assignments(reading_assigns, prog_assigns, exams):
    response = requests.get(canvas_endpoint + '/assignments?per_page=100', headers=headers).json()
    for assignment in response:
        #TODO: determine a better condition to only include reading and programming assignments
        #print(assignment['name'])
        if str(assignment['name']).lower() in reading_assigns or str(assignment['name']).lower() in prog_assigns or str(assignment['name']).lower() in exams:
            assignment_info.update({str(assignment['name']): [str(assignment['id']), dt_frmt(str(assignment['due_at']))]})
            #print('Assignment - ' + str(assignment['name']) + ': ' + str(assignment['id']) + ', ' + str(dt_frmt(str(assignment['due_at']))))

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
    get_students()
    re_grades = zg.get_readings()
    data = [{'grade_data': {}}, {'grade_data': {}}]
    failed_eids = set()
    responses = []
    for i in range(len(data)): 
        for student in re_grades:
            try:
                data[i]['grade_data'].update({student_info[student.lower()]: {'posted_grade': re_grades[student][i]}})
            except Exception as e:
                failed_eids.add(student)
        responses.append(requests.post(canvas_endpoint + '/assignments/' + assignment_info['E' + str(i+1)][0] + '/submissions/update_grades', headers=headers, json=(data[i])))
    #Testing purposes (determine if requests was successful and which eids failed)
    print(str(responses) + '\n' + str(failed_eids))
    pass

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

if __name__ == '__main__':
    prog_assignments = set(input('Enter which programming assignments are being graded: ').split())
    reading_assignments = set(input('Enter which reading assignments are being graded: ').split())
    get_assignments(prog_assignments, reading_assignments, [])
    update_assignments()
    # update_readings()
    
    