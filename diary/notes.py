from tkinter import messagebox
from tkinter.simpledialog import Dialog
from tkinter import *


class TextDialog(Dialog):
    def __init__(self, title, prompt,
                 widget=None,
                 edit=None,
                 parent=None):
        self.text = None
        self.prompt = prompt
        self.parent = parent
        self.edit_text = edit
        self.widget = widget

        Dialog.__init__(self, parent, title)

    def buttonbox(self):
        box = Frame(self)

        w = Button(box, text="OK", width=10, command=self.ok)
        w.pack(side=LEFT, padx=5, pady=5)
        w = Button(box, text="Cancel", width=10, command=self.cancel)
        w.pack(side=LEFT, padx=5, pady=5)
        if self.widget is not None:
            w = Button(box, text="Delete", width=10, command=self.delete)
            w.pack(side=LEFT, padx=5, pady=5)

        self.bind("<Control-Return>", self.ok)
        self.bind("<Escape>", self.cancel)

        box.pack()

    def destroy(self):
        Dialog.destroy(self)

    def delete(self):
        if messagebox.askokcancel("Удаление", "Вы действительно хотите удалить данную запись?"):
            self.widget.destroy()
            self.result = ' '
            Dialog.destroy(self)

    def body(self, master):
        w = Label(master, text=self.prompt, justify=LEFT)
        w.grid(row=0, padx=5, sticky=W)

        self.text = Text(master)
        self.text.grid(row=1, padx=5, sticky=NW)

        if self.edit_text is not None:
            self.text.insert(1.0, self.edit_text)
            self.result = self.edit_text
        else:
            self.result = ' '
        return self.text

    def validate(self):
        self.result = self.text.get(1.0, END)
        if not str(self.result).isspace():
            i = -1
            while self.result[i] == '\n':
                i -= 1
            if i < -1:
                self.result = self.result[:i + 1]
        return 1


class Notes:
    def __init__(self, tab: Frame):
        self.tab = tab
        self.notes = list()
        self.notes_n = 0

    def add_note(self, note_text: str):
        if note_text is not None and not note_text.isspace():
            note = Note(note_text)
            note_label = Label(self.tab, text=note.label_text,
                               justify='left', width=25, height=2)
            note_label.grid(column=self.notes_n % 4, row=self.notes_n // 4 + 1, padx=4, pady=3, sticky=W + E)
            self.notes.append(note)
            note_label.bind("<Double-1>", self.edit_note)
            self.notes_n += 1

    def edit_note(self, event):
        for note in self.notes:
            if note.label_text == event.widget["text"]:
                d = TextDialog("Редактирование заметки", "Введите текст заметки", event.widget, edit=note.text,
                               parent=self.tab)
                if not d.result.isspace():
                    note.text = str(d.result)
                    note.label_text = make_less(note.text)
                    event.widget["text"] = note.label_text
                else:
                    self.notes.remove(note)
                    self.notes_n -= 1
                break


def make_less(edit_text):
    result = edit_text
    if len(edit_text) > 18 or edit_text.count('\n') != 0:
        if edit_text.count('\n') == 0:
            result = edit_text[:18] + '...'
        else:
            result = edit_text.split('\n')[0][:18] + '...'
    return result


class Note:
    def __init__(self, text: str):
        self.text = text
        self.label_text = make_less(text)


def ask_dialog(title, prompt, parent):
    d = TextDialog(title, prompt, parent=parent)
    return d.result

