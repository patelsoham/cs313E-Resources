from dotenv import load_dotenv
load_dotenv()

import os
import json
import time
import requests
import submission as sub

hackerrank_key = os.getenv('HACKERRANK_KEY')
hackerrank_endpoint = os.getenv('HACKERRANK_ENDPOINT')
headers = {'Authorization': 'Bearer {}'.format(hackerrank_key), 'content-type': 'application/json'}
#'Assignment' in test['name'].split(' ')[0] and (['1', '2', '3', '4', '5', '6', '7', '9', '10'].count(test['name'].split(' ')[1]) != 0)

#Extracts name and id of Assignment tests (eventually will also include exams)
name_id = lambda info, assignments: {shorten_name(test): test['id'] for test in info if 'Assignment' in test['name'].split(' ')[0] and (['14'].count(test['name'].split(' ')[1]) != 0)}
file_path = lambda submission: 'assignment_reports/' + (submission.assignment_name.lower()) + '/' + (submission.eid) + '_' + (submission.assignment_name) + '_report.pdf'
shorten_name = lambda test: str(test['name'][:12][0] + test['name'].split(' ')[1])
#Get dictionary of test names and ids as key value pairs

def get_tests(assignments):
    try:
        print(assignments)
        return name_id(requests.get(hackerrank_endpoint + 'tests?limit=30&offset=0', headers=headers).json()['data'], assignments)
    except Exception as e:
        print('Failed to get all tests.')
        print(e)
        return None
    
#get dictionary of assignment names and an array of student submissions as key value pairs
def get_submissions(assignments, download):
    test_ids = get_tests(assignments)
    student_info = {}
    responses = {}
    for test in test_ids:
        student_info.update({test: get_assignment_submissions(test, test_ids[test])})
    if download:
        for assignment in student_info:
            for submission in student_info[assignment]:
                try:
                    responses.update({submission.eid: download_report(submission)})
                    if submission.partner_eid != None:
                        responses.update({submission.partner_eid: download_report(submission)})
                except Exception as e:
                    print('Failed on ' + submission.eid + '\n' + str(e))
        print('Number of reports successfully downloaded: ' + str(sum(1 for resp in responses.values() if resp.ok)) + '\n')
        print(str(responses) + '\n')
    #write_output(student_info)
    return student_info

#Get one assignment's submissions
def get_assignment_submissions(assignment_name, assignment_id):
    result = []
    initialized_submissions = set()
    try:
        submissions = requests.get(hackerrank_endpoint + 'tests/' + assignment_id + '/candidates?limit=100&offset=0', headers=headers).json()['data']
        for entry in submissions:
            if entry['status'] == 7:
                #Get Both Student and Partner's Submissions (If there is a partner one)
                cur_submission = sub.Submission(get_eid(entry['candidate_details']), get_partner_eid(entry['candidate_details']), assignment_name, entry['percentage_score'], entry['plagiarism_status'], entry['pdf_url'], entry['attempt_endtime'])
                #Check which submission has a higher score and update the result list accordingly
                if cur_submission in initialized_submissions:
                    added_submission = result.pop(result.index(cur_submission))
                    result.append(max(cur_submission, added_submission, key=lambda x: x.score))
                else:
                    result.append(cur_submission)
                    initialized_submissions.add(cur_submission)
    except Exception as e:
        print('Failed on ' + assignment_name + '\n' + str(e))
    return result


def write_output(result):
    fptr = open('static_data/assignment_grader_output.txt', 'w')
    for test in result:
        fptr.write('____________________________________________________________________________________' + str(test) + '____________________________________________________________________________________\n')
        for entry in result[test]:
            fptr.write(str(entry) + '\n')

#get student eid
def get_eid(candidate_details):
    for detail in candidate_details:
        if detail['title'] == 'EID':
            return detail['value'].strip()
    return None

#get partner eid if there is one
def get_partner_eid(candidate_details):
    for detail in candidate_details:
        if detail['title'] == 'Partner EID':
            if detail['value'] == 'anh368':
                return os.getenv('MISTYPED_EID').strip()
            else:
                return detail['value'].strip()
    return ''

def download_report(submission): 
    response = requests.get(submission.pdf, headers=headers, allow_redirects=True)
    open(file_path(submission), 'wb').write(response.content)
    return response

if __name__ == '__main__':
    get_tests(['10'])
    

    

    
    