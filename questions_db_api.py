import requests
from html import unescape

class GetQuestions:
    def __init__(self, params):
        self.params = params
        self.api_output = requests.get('https://opentdb.com/api.php', params=self.params).json()
        self.i = 0

    def print_question(self):
        if self.i < self.params['amount']:
            self.q = self.api_output['results'][self.i]
            print(self.q)
            self.i += 1
            return unescape(self.q['question'])

    def check_answer(self, window, canvas, pick):
        if self.q['correct_answer'] != pick:
            canvas.configure(window, bg="red")
        else:
            canvas.configure(window, bg="green")



