from tkinter.simpledialog import askstring
from diary.notes import make_less, Note, TextDialog
from tkinter import *


class Subjects:
    def __init__(self, tab: Frame):
        self.tab = tab
        self.subject_list = list()
        self.checked = list()
        self.tasks = list()

    def add_subject(self, subject_name: str):
        subject_name = make_less(subject_name)
        button = Button(self.tab, text=subject_name, relief='groove', height=2, width=20)
        button.grid(column=0,
                    row=len(self.subject_list) + 1,
                    padx=4,
                    pady=3)
        button.bind("<Button-1>", self.check)
        self.subject_list.append(button)

    def check(self, event):
        if event.widget['relief'] == 'groove':
            event.widget['relief'] = 'sunken'
            if self.checked.count(event.widget) == 0:
                self.checked.append(event.widget)
        else:
            event.widget['relief'] = 'groove'
            self.checked.remove(event.widget)

    def nullify(self):
        for button in self.checked:
            button['relief'] = 'groove'
        self.checked.clear()

    def add_homework(self, homework_text, homework_subjects):
        if homework_text is not None and not homework_text.isspace():
            homework = Homework(homework_text, homework_subjects)
            homework_label = Label(self.tab, text=homework.label_text,
                                   justify='left', width=25, height=2)
            homework_label.grid(column=len(self.tasks) % 3 + 1, row=len(self.tasks) // 3 + 1, padx=4, pady=3, sticky=W + E)
            self.tasks.append(homework)
            homework_label.bind("<Double-1>", self.edit_homework)

    def edit_homework(self, event):
        for task in self.tasks:
            if task.label_text == event.widget["text"]:
                d = TextDialog("Редактирование ДЗ", task.homework_subjects, edit=task.text,
                               parent=self.tab)
                task.text = str(d.result)
                task.label_text = make_less(task.text)
                event.widget["text"] = task.label_text
                break


class Homework(Note):
    def __init__(self, homework_text, homework_subjects):
        self.homework_subjects = homework_subjects
        Note.__init__(self, homework_text)
