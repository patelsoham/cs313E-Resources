from dotenv import load_dotenv
load_dotenv()

import os
import json
import time
import requests
import submission


#TODO: filter hackerrank tests (in name_id) to ensure only assignments from this semester are considered

hackerrank_key = os.getenv('HACKERRANK_KEY')
hackerrank_endpoint = os.getenv('HACKERRANK_ENDPOINT')
#Extracts name and id of Assignment tests (eventually will also include exams)
name_id = lambda info: {test['name'][:12]: test['id'] for test in info if 'Assignment' in test['name'].split(' ')[0]}

#Get dictionary of test names and ids as key value pairs
def get_tests():
    try:
        temp = name_id(requests.get(hackerrank_endpoint + 'tests?limit=20&offset=0', auth=(hackerrank_key, '')).json()['data'])
    except Exception as e:
        print('Failed to get all tests.')
        print(e)
    return temp

#get dictionary of assignment names and an array of student submissions as key value pairs
def get_students():
    test_ids = get_tests()
    student_info = {}
    for test in test_ids:
        student_info.update({test: []})
        try:
            submissions = requests.get(hackerrank_endpoint + 'tests/' + test_ids[test] + '/candidates?limit=59&offset=0', auth=(hackerrank_key, '')).json()['data']
            for entry in submissions:
                if entry['status'] == 7:
                    details = entry['candidate_details']
                    temp = submission.Submission(details[0]['value'], entry['score'], entry['plagiarism_status'], entry['pdf_url'])
                    student_info[test].append(temp)
                    if len(details[2]['value']) > 0:
                        student_info[test].append(submission.Submission(details[2]['value'], entry['score'], entry['plagiarism_status'], entry['pdf_url']))
                else:
                    print('Code not submitted')
        except Exception as e:
            print('Failed on ' + test + ': ' + test_ids[test])
            print(e)
    return student_info


if __name__ == '__main__':
    result = get_students()
    for test in result:
        for entry in result[test]:
            print(str(entry))
    