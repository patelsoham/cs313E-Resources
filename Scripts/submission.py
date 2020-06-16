import datetime


class Submission():
    def __init__(self, eid, score, plagiarism, pdf, submit_time):
        self.eid = eid
        self.score = score
        self.plagiarism = plagiarism
        self.pdf = pdf
        self.submit_time = datetime.datetime.strptime(submit_time,'%Y-%m-%dT%H:%M:%S+%f').date()
    
    def __str__(self):
        return 'eid: {self.eid}, score: {self.score}, plagiarism: {self.plagiarism}, pdf_url: {self.pdf}, submit_time: {self.submit_time}'.format(self=self)
        