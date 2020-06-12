class Submission():
    def __init__(self, eid, score, plagiarism, pdf):
        self.eid = eid
        self.score = score
        self.plagiarism = plagiarism
        self.pdf = pdf
    
    def __str__(self):
        return 'eid: {self.eid}, score: {self.score}, plagiarism: {self.plagiarism}, pdf_url: {self.pdf}'.format(self=self)
        