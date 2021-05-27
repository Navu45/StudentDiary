import os
from tkinter import *
import tkinter.ttk as ttk

from diary.schedule import *


def run_app():
    """Запускает десктопное приложение

                """

    def clicked1():
        print(str(txt1.get()))
        t = str(txt1.get()).upper()
        Label(tab1, text='Группа : ' + t).grid(column=2, row=0, padx=4, pady=3, sticky='nw')
        try:
            schedule_list = show_schedule_for_week(t, datetime.datetime.today())
            for i in range(6):
                if i < 3:
                    Label(tab1, text=schedule_list[i], background='white', justify='left', wraplength='325').grid(
                        column=i,
                        row=1,
                        padx=4,
                        pady=3,
                        sticky='nw')
                else:
                    Label(tab1, text=schedule_list[i], background='white', justify='left', wraplength='325').grid(
                        column=i % 3,
                        row=2,
                        padx=4,
                        pady=3,
                        sticky='nw')
        except Exception:
            Label(tab1, text="Некорректный ввод!").grid(column=0, row=1, padx=4, pady=3, sticky='nw')
        return 0

    # get_schedule_from_mirea()
    window = Tk()

    window.title("Дневник")
    window.geometry("1000x700")

    tab_control = ttk.Notebook(window)

    tab1 = ttk.Frame(tab_control)
    tab_control.add(tab1, text="Расписание")
    tab2 = ttk.Frame(tab_control)
    tab_control.add(tab2, text="Домашнее задание")
    tab3 = ttk.Frame(tab_control)
    tab_control.add(tab3, text="Заметки")

    # ttk.Entry(tab1, width=20).grid(column=1, row=2, padx=4, pady=3, sticky='w')

    txt1 = StringVar()
    txt_entry = Entry(tab1, textvariable=txt1).grid(column=0, row=0, padx=4, pady=3, sticky='nw')
    btn1 = Button(tab1, text='Выбрать', command=clicked1, width=25).grid(column=1, row=0, padx=4, pady=3, sticky='nw')
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

    tab_control.pack(expand=True, fill=BOTH)
    window.mainloop()


if __name__ == '__main__':
    run_app()
