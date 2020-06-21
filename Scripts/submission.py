import datetime
import math


class Submission():
    def __init__(self, eid = None, assignment_name = None, score = 0.0, plagiarism = None, pdf = None, submit_time = None):
        self.eid = eid
        self.assignment_name = assignment_name
        self.score = score
        self.plagiarism = plagiarism
        self.pdf = pdf
        self.submit_time = datetime.datetime.strptime(submit_time,'%Y-%m-%dT%H:%M:%S+%f') if submit_time != None else submit_time

    #update score based on when turned in.
    def update_score(self, due_date):
        try:
            diff = math.ceil((self.submit_time - due_date - datetime.timedelta(minutes=59)).total_seconds()/86400)
            print('Difference in days: ' + str(diff))
            self.score -= (diff*10) if diff > 0 else 0
            self.score = self.score if self.score > 0 else 0.0
        except Exception as e:
            print('Unable to apply late penalty. Assignment never submitted for ' + str(self))
            self.score = 0.0
        
    def __str__(self):
        return 'eid: {self.eid}, assignment name: {self.assignment_name}, score: {self.score},  plagiarism: {self.plagiarism}, pdf_url: {self.pdf}, submit_time: {self.submit_time}'.format(self=self)
        