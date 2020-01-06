# Word Checker, version 1.0
# (ɔ) Dmitriy Antonenko, may 2017

import tkinter as tk
from tkinter import ttk
from tkinter import scrolledtext

resulting_list = []

class Standardized_Word:
    """String containing only russian lower leters. All other symbols replaced."""
    
    def __init__(self, word):
        word = word.lower()
        for char in word:
            if ord(char) not in range(1072, 1104) and ord(char) != 1105:
                word = word.replace(char, '')
        self.word = word

    def __str__(self):
        return self.word


def checkWord(given_word,checking_word):
    for char in checking_word:
        if char in given_word and checking_word.count(char) <= given_word.count(char) and checking_word != given_word:
            continue
        else:
            return False
    return checking_word

def form_result(long_word):

    dictionary = open("word_rus2.txt", "r")

    for word in dictionary:
        word = str(Standardized_Word(word))
        if checkWord(str(long_word),word) != False:
            resulting_list.append(word)

    dictionary.close()
    
class Gui:

    def __init__(self):
        self.application_window = tk.Tk()
        self.entry_value = tk.StringVar()
        self.entry_value.set('')
        self.create_widgets()

    def create_widgets(self):

        entering_space = ttk.LabelFrame(self.application_window, text='Введите слово')
        entering_space.grid(row=1, column=1, sticky=tk.W, pady=5, padx=10)

        enter_word = ttk.Entry(entering_space, width=35)
        enter_word.grid(row=1, column=1, sticky=tk.E + tk.W + tk.N, pady=7, padx=10)
        enter_word['textvariable'] = self.entry_value
        enter_word.bind("<Return>", self.start_checking)

        start_button = ttk.Button(entering_space, text=" Найти ", command=self.start_checking)
        start_button.grid(row=1, column=2, sticky=tk.E + tk.W + tk.N, pady=5, padx=10)

        output_space = ttk.LabelFrame(self.application_window, text='Результат')
        output_space.grid(row=2, column=1, sticky=tk.W, pady=5, padx=10)
        
        output_comment = ttk.Label(output_space, text='Программа ожидает введения слова')
        output_comment.grid(row=1, column=1, sticky=tk.W, pady=5, padx=10)

        output_window = scrolledtext.ScrolledText(output_space, padx=10, pady=10, width=50)
        output_window.grid(row=2, column=1, padx=10, pady=10)

    def start_checking(self, nonsense=0):
        #'nonsense' is the empty parameter needed only because without it the instruction 'enter_word.bind("<Return>", self.start_checking)' wasn't working 
        form_result(Standardized_Word(self.entry_value.get()))

        output_space = ttk.LabelFrame(self.application_window, text='Результат')
        output_space.grid(row=2, column=1, sticky=tk.W + tk.N, pady=5, padx=10)
        
        output_window = scrolledtext.ScrolledText(output_space, padx=10, pady=10, width=50)
        output_window.grid(row=2, column=1, padx=10, pady=10)
        output_window.delete(1.0, '1.end')
        
        resulting_text = ''
        for num in range (1, len(resulting_list) + 1):
            resulting_text = resulting_text + str(num) + '.' + '\t'
            resulting_text = resulting_text + resulting_list[num - 1]
            resulting_text = resulting_text + '\n'

        if int(str(len(resulting_list))[-1]) == 1 and len(resulting_list) != 11:
            comment_end = 'другое слово'
        elif int(str(len(resulting_list))[-1]) in range(2, 5) and len(resulting_list) not in range (12, 15):
            comment_end = 'других слова'
        else:
            comment_end = 'других слов'

        if len(resulting_list) != 0:
            comment_text = 'Из букв слова ' + '"' + str(Standardized_Word(self.entry_value.get())) + '"' + ' можно составить ' + str(len(resulting_list)) + ' ' + comment_end + ':'
            output_comment = ttk.Label(output_space, text=comment_text)
            output_comment.grid(row=1, column=1, sticky=tk.W + tk.N, pady=5, padx=10)
        else:
            comment_text = 'Из букв введённого слова невозможно составить ни одного другого слова.'
            output_comment = ttk.Label(output_space, text=comment_text)
            output_comment.grid(row=1, column=1, sticky=tk.W + tk.N, pady=5, padx=10)
        
        global resulting_list
        resulting_list = []
        output_window.insert(1.0, resulting_text)

        
# Create the entire GUI program
program = Gui()

# Start the GUI event loop
program.application_window.mainloop()
