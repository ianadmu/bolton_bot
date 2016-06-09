import os.path
import random

class ExplanationManager(object):

    def __init__(self):
        self.explanation_file = open(os.path.join('./resources', 'explanations.txt'), 'r')
        self.explanations = self.explanation_file.readlines()
        
    def get_explanation(self):
        return random.choice(self.explanations)
        