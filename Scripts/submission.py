import datetime
import math

parse_time = lambda str_time: datetime.datetime.strptime(str_time,'%Y-%m-%dT%H:%M:%S+%f') 

class Submission():
    def __init__(self, eid = None, assignment_name = None, score = 0.0, plagiarism = None, pdf = None, submit_time = None):
        self.eid = eid
        self.assignment_name = assignment_name
        self.score = score
        self.plagiarism = plagiarism
        self.pdf = pdf
        self.submit_time = parse_time(submit_time) if type(submit_time) is str else submit_time

    def get_score(self):
        return self.score

    def get_eid(self):
        return self.eid

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
    
    def get_partner_submission(self, partner_eid):
        return Submission(partner_eid, self.assignment_name, self.score, self.plagiarism, self.pdf, self.submit_time)
        
    def __str__(self):
        return 'eid: {self.eid}, assignment name: {self.assignment_name}, score: {self.score},  plagiarism: {self.plagiarism}, pdf_url: {self.pdf}, submit_time: {self.submit_time}'.format(self=self)
        