from tkinter import *
from functools import partial
import pandas

FONT_NAME = "Courier"
SECONDS = 60
wordlist = []
prog_wordlist = []

#---------------TIMER------------------
def timer_start(seconds):
    label['text'] = 'Type!'
    label_timer.config(text=f'{seconds} sec')
    word_list_label.config(font=(FONT_NAME, 30, 'bold'))

    if len(wordlist) == len(prog_wordlist):
        show_words()

    if seconds != 0:
        window.after(1000, timer_start, seconds - 1)
    elif seconds == 0:
        label['text'] = 'One more time?'
        label_timer.config(text=f'{seconds} sec', fg='yellow')
        wrong_w = compare()

        str = ""
        for ele in wordlist:
            str += ele

        CPM = len(str)
        WPM = count_right_words()
        if wrong_w == '':
            text = f'Your CPM is {CPM} and WPM is {WPM}.\nAnd there is no wrong word!'
        else:
            text = f'Your CPM is {CPM} and WPM is {WPM}. Mistakes:\n{wrong_w}'
        word_list_label.config(text=text, font=(FONT_NAME, 15))
        print(wordlist)
        print(prog_wordlist)

#---------------FIND WRONG WORDS----------
def compare():
    wrong_words = []
    for n in range(len(prog_wordlist[:len(wordlist)])):
        if prog_wordlist[n] != wordlist[n]:
            wrong_words.append(f'· Instead of "{prog_wordlist[n]}" you typed "{wordlist[n]}"\n')
    str = ""
    for ele in wrong_words:
        str += ele
    return str

#---------------COUNT RIGHT WORDS--------------
def count_right_words():
    right_words = []
    for n in range(len(prog_wordlist[:len(wordlist)])):
        if prog_wordlist[n] == wordlist[n]:
            right_words.append(wordlist[n])
    str = ""
    for ele in right_words:
        str += ele
    return round(len(str) / 5)



#---------------SHOW WORDS-------------------
def show_words():
    global prog_wordlist
    data = pandas.read_csv('words.csv')
    new_list_of_words = list(data['words'].sample(5))
    prog_wordlist = prog_wordlist + new_list_of_words
    word_list_label['text'] = new_list_of_words

#--------------USER WORD LIST--------------
def add_to_wordlist(word):
    global wordlist
    wordlist.append(entry.get())
    if entry.get() in prog_wordlist:
        label_timer.config(fg='green')
    else:
        label_timer.config(fg='red')
    entry.delete(0, 'end')
    return("break")

#--------------EMPTY LISTs--------------
def empty_lists():
    global wordlist
    global prog_wordlist
    wordlist = []
    prog_wordlist = []

timer = partial(timer_start, SECONDS)

#--------------GUI----------------
window = Tk()
window.title('Typing test')
window.config(padx=70, pady=50, bg='pink')

label = Label(text='Welcome to typing test!', font=(FONT_NAME, 50, 'bold'))
label.config(bg='pink')
label.grid(row=0, column=1)

label_timer = Label(text='60 sec', font=(FONT_NAME, 30, 'bold'))
label_timer.config(fg='yellow', bg='pink')
label_timer.grid(row=1, column=1)

word_list_label = Label(text='Tab start to begin', font=(FONT_NAME, 30, 'bold'))
word_list_label.config(bg='pink')
word_list_label.grid(row=2, column=1)

entry = Entry(highlightthickness=0)
entry.insert(END, 'Put words here')
entry.bind('<space>', add_to_wordlist)
entry.focus()
entry.grid(row=3, column=1)

start_button = Button(text='Start', highlightthickness=0, command=lambda: [empty_lists(), show_words(),
                                                                           timer(), entry.delete(0, 'end')])
start_button.grid(row=4, column=1)

window.mainloop()