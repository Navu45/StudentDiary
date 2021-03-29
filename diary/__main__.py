from tkinter import *
import tkinter.ttk as ttk

def run_app():
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

    tab_control.pack(expand=True, fill=BOTH)
    window.mainloop()

if __name__ == '__main__':
    run_app()