from tkinter import *
import requests
from questions_db_api import GetQuestions

CATEGORIES = requests.get("https://opentdb.com/api_category.php").json()

BG_COLOR = "#648776"
PLATE_COLOR = "#014021"
TRUE_COLOR = "#00bf00"
FALSE_COLOR = "#b81414"

params = {"amount": 10, "category": None, "type": 'boolean'}

window = Tk()
window.title("Quiz")
window.config(padx=40, pady=60, bg=PLATE_COLOR)

end = False

def main():
    def finish():
        global end
        end = True
        plate.itemconfigure(question_window, text=f"\tTHE END\t\nYour score: {questions.score}/{params['amount']} ({(questions.score/params['amount'])*100}%)\nDo you want to play again?")
    def answer(pick):
        true_pick.config(state='disabled')
        false_pick.config(state='disabled')
        def change_question():
            true_pick.config(state='normal')
            false_pick.config(state='normal')
            if questions.i < params['amount']:
                plate.config(bg=PLATE_COLOR)
                plate.itemconfigure(question_window, text=questions.print_question())
            else:
                finish()
        if not end:
            if questions.check_answer(pick):
                plate.config(bg=TRUE_COLOR)
                questions.score += 1
            else:
                plate.config(bg=FALSE_COLOR)
        else:
            if pick == "True":
                questions.i = 0
                blackout()
                return set_params()
            else:
                window.destroy()
        scoreboard.config(text=f'Score: {questions.score}')
        window.after(2000, change_question)

    questions = GetQuestions(params)
    window.config(bg=BG_COLOR)
    scoreboard = Label(text=f"Score: 0", font=("Comic Sans MS", 16, "bold"), bg=BG_COLOR, fg="white")
    scoreboard.grid(row=0, column=1)
    plate = Canvas(width=600, height=500, bg=PLATE_COLOR)
    question_window = plate.create_text(300, 250, width=500, text=questions.print_question(), fill="white", font=("Comic Sans MS", 16, "bold"))
    true_pick = Button(bg=BG_COLOR, image=true, highlightthickness=0, command= lambda: answer("True"))
    false_pick = Button(bg=BG_COLOR, image=false, highlightthickness=0, command= lambda: answer("False"))
    plate.grid(row=1, columnspan=2)
    true_pick.grid(row=2, column=0, pady=(30, 0))
    false_pick.grid(row=2, column=1, pady=(30, 0))

def blackout():
    global end
    for widget in window.winfo_children():
        widget.destroy()
    window.config(bg=PLATE_COLOR)
    end = False

def choosen_category(category):
    global params
    params['category'] = category
    blackout()
    return main()

def set_amount(amount):
    global params
    params['amount'] = amount

def set_params():
    Label(text='How many questions do you want challange with?', font=("Comic Sans MS", 22, "bold"), bg=PLATE_COLOR, fg="white").grid(row=0, columnspan=2)
    var = StringVar(window)
    amount_options = [q_amount for q_amount in range(5,51,5)]
    amount_choice = OptionMenu(window, var, *amount_options, command= lambda var=var: set_amount(var))
    var.set(amount_options[1])
    amount_choice.grid(row=1, columnspan=2)
    amount_choice.config(highlightthickness=0)
    Label(text="Choose category:", font=("Comic Sans MS", 22, "bold"), bg=PLATE_COLOR, fg="white").grid(row=2, columnspan=2)
    for num, category in enumerate(CATEGORIES["trivia_categories"]):
        choice_name = category['name']
        choice_id = category['id']
        Button(text=choice_name.split(": ")[-1], width=45, command=lambda choice_id=choice_id: choosen_category(choice_id)).grid(row=num//2+3, column=1 if num%2 == 0 else 0, pady=4, sticky= E if num%2 == 0 else W)

true = PhotoImage(file="images/true.png")
false = PhotoImage(file="images/false.png")

set_params()

window.mainloop()