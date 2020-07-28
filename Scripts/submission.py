import datetime
import math

parse_time = lambda str_time: datetime.datetime.strptime(str_time,'%Y-%m-%dT%H:%M:%S+%f') 

class Submission():
    def __init__(self, eid = None, partner_eid = None, assignment_name = None, score = 0.0, plagiarism = None, pdf = None, submit_time = None):
        self.eid = eid
        self.partner_eid = partner_eid if len(partner_eid) > 0 else None
        self.assignment_name = assignment_name
        self.score = score
        self.plagiarism = plagiarism
        self.pdf = pdf
        self.submit_time = parse_time(submit_time) if type(submit_time) is str else submit_time
    
    def get_score(self):
        return self.score

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

    def __eq__ (self, other):
        if isinstance(other, Submission):
            return (self.eid == other.eid and self.partner_eid == other.partner_eid) or (self.eid == other.partner_eid and self.partner_eid == other.eid)
        return NotImplemented

    def __hash__(self):
        return hash(self.eid) + hash(self.partner_eid)
        
    def __str__(self):
        return 'eid: {self.eid}, partner eid: {self.partner_eid}, assignment name: {self.assignment_name}, score: {self.score},  plagiarism: {self.plagiarism}, pdf_url: {self.pdf}, submit_time: {self.submit_time}'.format(self=self)
        