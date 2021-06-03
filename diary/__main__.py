import tkinter.ttk as ttk
from tkinter import *

from diary.homework import Subjects
from diary.schedule import *
from diary.notes import ask_dialog, Notes
from tkinter.simpledialog import askstring


def run_app():
    """Запускает десктопное приложение

                """

    def clicked1():
        print(str(txt1.get()))
        t = str(txt1.get()).upper()
        Label(tab1, text='Группа : ' + t, font='Arial 14', bg='white').grid(column=2, row=0, padx=4, pady=3,
                                                                            sticky='nw')
        try:
            schedule_list = show_schedule_for_week(t, datetime.datetime.today())
            for i in range(6):
                if i < 3:
                    Label(tab1, text=schedule_list[i], font='Arial 10', justify='left', wraplength='325').grid(
                        column=i,
                        row=1,
                        padx=4,
                        pady=3,
                        sticky='nw')
                else:
                    Label(tab1, text=schedule_list[i], font='Arial 10', justify='left', wraplength='325').grid(
                        column=i % 3,
                        row=2,
                        padx=4,
                        pady=3,
                        sticky='nw')
        except Exception:
            Label(tab1, font='Arial 10', bg='white', text="Некорректный ввод!").grid(column=0, row=1, padx=4, pady=3,
                                                                                     sticky='nw')
        return 0

    # get_schedule_from_mirea()
    window = Tk()

    window.title("StudentDiary")
    window.geometry("1000x700")

    s1 = ttk.Style()
    s1.configure('My.TFrame', background='white')

    tab_control = ttk.Notebook(window)

    tab1 = ttk.Frame(tab_control, style='My.TFrame')
    tab_control.add(tab1, text=f'{"Расписание": ^30s}')

    tab2 = ttk.Frame(tab_control, style='My.TFrame')
    tab_control.add(tab2, text=f'{"Домашнее задание": ^30s}')

    tab3 = ttk.Frame(tab_control, style='My.TFrame')
    tab_control.add(tab3, text=f'{"Заметки": ^30s}')

    # ttk.Entry(tab1, width=20).grid(column=1, row=2, padx=4, pady=3, sticky='w')

    txt1 = StringVar()
    txt_entry = Entry(tab1, textvariable=txt1).grid(column=0, row=0, padx=4, pady=3, sticky='nw')
    btn1 = Button(tab1, text='Выбрать', command=clicked1, width=25)
    btn1.grid(column=1, row=0, padx=4, pady=3, sticky='nw')

    # lbl0 = Label(tab1, text='').grid(column=2, row=0, padx=4, pady=3, sticky='nw')
    # schedule_list = show_schedule_for_week("ИКБО-03-19", datetime.datetime.today())
    #
    # for i in range(6):
    #     if i < 3:
    #         Label(tab1, text=schedule_list[i], background='white', justify='left', wraplength='295').grid(column=i,
    #                                                                                                       row=1,
    #                                                                                                       padx=4,
    #                                                                                                       pady=3,
    #                                                                                                       sticky='nw')
    #     else:
    #         Label(tab1, text=schedule_list[i], background='white', justify='left', wraplength='295').grid(
    #             column=i % 3,
    #             row=2,
    #             padx=4,
    #             pady=3,
    #             sticky='nw')

    notes = Notes(tab3)
    subjects = Subjects(tab2)

    set_notes_page(notes, window)
    set_homework_page(subjects, window)
    tab_control.pack(expand=True, fill=BOTH)
    window.mainloop()


def set_homework_page(subjects, window: Tk):
    def add_tag():
        subject_name = str(askstring("Создание тега", "Введите название предмета (тег)"))
        if subject_name is not None and not subject_name.isspace() and subject_name.isalnum():
            subjects.add_subject(subject_name)

    def add_homework():
        homework_subjects = ' + '.join([button.cget('text') for button in subjects.checked])
        homework_text = str(ask_dialog("Создание ДЗ", homework_subjects, window))
        subjects.add_homework(homework_text, homework_subjects)
        subjects.nullify()

    btn3 = Button(subjects.tab, text='Добавить предмет', command=add_tag, width=25)
    btn3.grid(column=0, row=0, padx=4, pady=3, sticky=W + E)
    btn4 = Button(subjects.tab, text='Добавить ДЗ', command=add_homework, width=25)
    btn4.grid(column=1, row=0, padx=4, pady=3, sticky=W + E)


def set_notes_page(notes, window: Tk):
    def add_note():
        note_text = str(ask_dialog("Создание заметки", "Введите текст заметки", window))
        notes.add_note(note_text)

    btn2 = Button(notes.tab, text='Создать заметку', command=add_note, width=25)
    btn2.grid(column=0, row=0, padx=4, pady=3, sticky=W + E)
    window.bind('<Control-n>', add_note)


if __name__ == '__main__':
    run_app()
