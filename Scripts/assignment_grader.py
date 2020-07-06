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

#Extracts name and id of Assignment tests (eventually will also include exams)
name_id = lambda info: {test['name']: test['id'] for test in info if 'Assignment' in test['name'].split(' ')[0] and (['4', '5', '6'].count(test['name'].split(' ')[1]) != 0)}
file_path = lambda submission: 'hackerrank_reports/' + (submission.assignment_name.lower()) + '/' + (submission.eid) + '_' + (submission.assignment_name) + '_report.pdf'
#Get dictionary of test names and ids as key value pairs

def get_tests():
    try:
        temp = name_id(requests.get(hackerrank_endpoint + 'tests?limit=20&offset=0', headers=headers).json()['data'])
        return temp
    except Exception as e:
        print('Failed to get all tests.')
        print(e)
        return None
    
#get dictionary of assignment names and an array of student submissions as key value pairs
def get_submissions():
    test_ids = get_tests()
    student_info = {}
    submitted_eids = set()
    responses = {}
    for test in test_ids:
        canvas_assign_name = test[:12][0] + test[:12].split(' ')[1]
        student_info.update({canvas_assign_name: []})
        submitted_eids.clear()
        try:
            submissions = requests.get(hackerrank_endpoint + 'tests/' + test_ids[test] + '/candidates?limit=59&offset=0', headers=headers).json()['data']
            for entry in submissions:
                if get_eid(entry['candidate_details']) not in submitted_eids:
                    if entry['status'] == 7:
                        #score and report have been generated (entry is ready)
                        cur_submission = sub.Submission(get_eid(entry['candidate_details']), canvas_assign_name, entry['percentage_score'], entry['plagiarism_status'], entry['pdf_url'], entry['attempt_endtime'])
                        student_info[canvas_assign_name].append(cur_submission)
                        #responses.update({cur_submission.eid: download_report(cur_submission)})
                        submitted_eids.add(cur_submission.eid)
                        if len(get_partner_eid(entry['candidate_details'])) > 3:
                            #there was a partner so add another submission obj for the partner.
                            partner_submission = cur_submission.get_partner_submission(get_partner_eid(entry['candidate_details']))
                            student_info[canvas_assign_name].append(partner_submission)
                            #responses.update({partner_submission.eid: download_report(partner_submission)})
                            submitted_eids.add(partner_submission.eid)
                    elif entry['status'] != 7:
                        #print('Code not submitted for ' + test + ': ' + str(get_eid(entry['candidate_details'])))
                        student_info[canvas_assign_name].append(sub.Submission(get_eid(entry['candidate_details']), canvas_assign_name))
        except Exception as e:
            print('Failed on ' + test + ': ' + test_ids[test])
            print(e)
    print('Number of reports successfully downloaded: ' + str(sum(1 for resp in responses.values() if resp.ok)) + '\n')
    #print(str(responses) + '\n')
    return student_info

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
    fptr = open('static_data/assignment_grader_output.txt', 'w')
    result = get_submissions()
    for test in result:
        fptr.write('__________________________________________' + str(test) + '__________________________________________\n')
        for entry in result[test]:
            fptr.write(str(entry) + '\n')
   

    

    
    