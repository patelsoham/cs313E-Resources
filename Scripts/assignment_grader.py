from dotenv import load_dotenv
load_dotenv()

import os
import json
import time
import requests
import submission

hackerrank_key = os.getenv('HACKERRANK_KEY')
hackerrank_endpoint = os.getenv('HACKERRANK_ENDPOINT')
#Extracts name and id of Assignment tests (eventually will also include exams)
name_id = lambda info: {test['name']: test['id'] for test in info if 'Assignment' in test['name'].split(' ')[0] and (['1', '2'].count(test['name'].split(' ')[1]) != 0)}

#Get dictionary of test names and ids as key value pairs
def get_tests():
    try:
        temp = name_id(requests.get(hackerrank_endpoint + 'tests?limit=20&offset=0', auth=(hackerrank_key, '')).json()['data'])
        print('Tests: ' + str(temp))
        return temp
    except Exception as e:
        print('Failed to get all tests.')
        print(e)
        return None
    
#get dictionary of assignment names and an array of student submissions as key value pairs
def get_students():
    test_ids = get_tests()
    student_info = {}
    for test in test_ids:
        student_info.update({test: []})
        try:
            headers = {'authorization': 'Bearer {}'.format(hackerrank_key), 'content-type': 'application/json'}
            submissions = requests.get(hackerrank_endpoint + 'tests/' + test_ids[test] + '/candidates?limit=59&offset=0', headers=headers).json()['data']
            for entry in submissions:
                if entry['status'] == 7:
                    #score and report have been generated (entry is ready)
                    temp = submission.Submission(get_eid(entry['candidate_details']), entry['percentage_score'], entry['plagiarism_status'], entry['pdf_url'], entry['attempt_endtime'])
                    student_info[test].append(temp)
                    if len(get_partner_eid(entry['candidate_details'])) > 3:
                        #there was a partner so add another submission obj for the partner.
                        student_info[test].append(submission.Submission(get_partner_eid(entry['candidate_details']), entry['percentage_score'], entry['plagiarism_status'], entry['pdf_url'], entry['attempt_endtime']))
                else:
                    print('Code not submitted for ' + test + ': ' + str(get_eid(entry['candidate_details'])))
        except Exception as e:
            print('Failed on ' + test + ': ' + test_ids[test])
            print(e)
    return student_info

#get student eid
def get_eid(candidate_details):
    for detail in candidate_details:
        if detail['title'] == 'EID':
            return detail['value']
    return None

#get partner eid if there is one
def get_partner_eid(candidate_details):
    for detail in candidate_details:
        if detail['title'] == 'Partner EID':
            return detail['value']
    return None

if __name__ == '__main__':
    result = get_students()
    for test in result:
        for entry in result[test]:
            print(str(entry))
    
    