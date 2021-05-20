import os
from tkinter import *
import tkinter.ttk as ttk

from diary.schedule import *

if os.environ.get('DISPLAY', '') == '':
    os.environ.__setitem__('DISPLAY', ':0.0')


def run_app():
    """Запускает десктопное приложение

                """
    get_schedule_from_mirea()
    window = Tk()

    window.title("Дневник")
    window.geometry("900x700")

    tab_control = ttk.Notebook(window)
    tab1 = ttk.Frame(tab_control)
    tab_control.add(tab1, text="Расписание")
    tab2 = ttk.Frame(tab_control)
    tab_control.add(tab2, text="Домашнее задание")
    tab3 = ttk.Frame(tab_control)
    tab_control.add(tab3, text="Заметки")

    # ttk.Entry(tab1, width=20).grid(column=1, row=2, padx=4, pady=3, sticky='w')

    schedule_list = show_schedule_for_week("ИКБО-03-19", datetime.datetime.today())

    for i in range(6):
        if i < 3:
            Label(tab1, text=schedule_list[i], background='white', justify='left', wraplength='250').grid(column=i + 1,
                                                                                                          row=2,
                                                                                                          padx=4,
                                                                                                          pady=3,
                                                                                                          sticky='n')
        else:
            Label(tab1, text=schedule_list[i], background='white', justify='left', wraplength='250').grid(
                column=i % 3 + 1,
                row=3,
                padx=4,
                pady=3,
                sticky='n')

    tab_control.pack(expand=True, fill=BOTH)
    window.mainloop()


if __name__ == '__main__':
    run_app()
