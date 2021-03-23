import requests
from html import unescape

class GetQuestions:
    def __init__(self, params):
        self.params = params
        self.api_output = requests.get('https://opentdb.com/api.php', params=self.params).json()
        self.i = 0
        self.score = 0
        print(self.api_output)

    def print_question(self):
        self.q = self.api_output['results'][self.i]
        self.i += 1
        return unescape(self.q['question'])

    def check_answer(self, pick):
        if self.q['correct_answer'] != pick:
            return False
        else:
            return True



