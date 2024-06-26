# This file was generated by the Tkinter Designer by Parth Jadhav
# https://github.com/ParthJadhav/Tkinter-Designer
import tkinter
from pathlib import Path

# from tkinter import *
# Explicit imports to satisfy Flake8
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage
import os
from tkinter import ttk

import datetime


def director_employees_menu(window, main_menu_f, employee_info_f,
                            fire_employee_f, hire_employee_f,
                            employee_list_on_select_f,
                            employee_types,
                            employee_types_on_select_f):
    executable_path = os.path.abspath(__file__)
    executable_directory = os.path.dirname(executable_path)
    widgets = {}

    def relative_to_assets(path: str) -> Path:
        return executable_directory + "/assets/director_employees_menu/" + path

    window.geometry("800x600")
    window.configure(bg="#67B293")

    canvas = Canvas(
        window,
        bg="#67B293",
        height=600,
        width=800,
        bd=0,
        highlightthickness=0,
        relief="ridge"
    )
    widgets['canvas'] = canvas

    canvas.place(x=0, y=0)
    image_image_1 = PhotoImage(
        file=relative_to_assets("image_1.png"))
    image_1 = canvas.create_image(
        374.0,
        300.0,
        image=image_image_1
    )
    widgets['image_image_1'] = image_image_1
    widgets['image_1'] = image_1

    combo_box = ttk.Combobox(canvas, values=employee_types)
    combo_box.place(x=47.0, y=47.0, width=256, height=51)
    widgets['combo_box_employee'] = combo_box
    combo_box.bind("<<ComboboxSelected>>", employee_types_on_select_f)

    image_image_2 = PhotoImage(
        file=relative_to_assets("image_2.png"))
    image_2 = canvas.create_image(
        575.0,
        308.0,
        image=image_image_2
    )
    widgets['image_image_2'] = image_image_2
    widgets['image_2'] = image_2

    listbox = tkinter.Listbox(canvas)
    listbox.bind('<<ListboxSelect>>', employee_list_on_select_f)
    listbox.place(x=14, y=138, width=321, height=393)
    widgets['listbox_employees'] = listbox

    entry_image_1 = PhotoImage(
        file=relative_to_assets("entry_1.png"))
    entry_bg_1 = canvas.create_image(
        575.5,
        136.0,
        image=entry_image_1
    )
    entry_1 = Entry(
        bd=0,
        bg="#D9D9D9",
        fg="#000716",
        highlightthickness=0
    )
    entry_1.place(
        x=429.0,
        y=117.0,
        width=293.0,
        height=36.0
    )
    widgets['entry_bg_1'] = entry_bg_1
    widgets['entry_name'] = entry_1

    entry_image_2 = PhotoImage(
        file=relative_to_assets("entry_2.png"))
    entry_bg_2 = canvas.create_image(
        575.5,
        204.5,
        image=entry_image_2
    )
    entry_2 = Entry(
        bd=0,
        bg="#D9D9D9",
        fg="#000716",
        highlightthickness=0
    )
    entry_2.place(
        x=429.0,
        y=186.0,
        width=293.0,
        height=35.0
    )
    widgets['entry_bg_2'] = entry_bg_2
    widgets['entry_surname'] = entry_2

    entry_image_3 = PhotoImage(
        file=relative_to_assets("entry_3.png"))
    entry_bg_3 = canvas.create_image(
        575.5,
        274.0,
        image=entry_image_3
    )
    entry_3 = Entry(
        bd=0,
        bg="#D9D9D9",
        fg="#000716",
        highlightthickness=0
    )
    entry_3.place(
        x=429.0,
        y=255.0,
        width=293.0,
        height=36.0
    )
    widgets['entry_bg_3'] = entry_bg_3
    widgets['entry_patronymic'] = entry_3

    entry_image_4 = PhotoImage(
        file=relative_to_assets("entry_4.png"))
    entry_bg_4 = canvas.create_image(
        575.5,
        343.0,
        image=entry_image_4
    )
    entry_4 = Entry(
        bd=0,
        bg="#D9D9D9",
        fg="#000716",
        highlightthickness=0
    )
    entry_4.place(
        x=429.0,
        y=324.0,
        width=293.0,
        height=36.0
    )
    widgets['entry_bg_4'] = entry_bg_4
    widgets['entry_salary'] = entry_4

    entry_image_5 = PhotoImage(
        file=relative_to_assets("entry_5.png"))
    entry_bg_5 = canvas.create_image(
        575.5,
        411.5,
        image=entry_image_5
    )
    entry_5 = Entry(
        bd=0,
        bg="#D9D9D9",
        fg="#000716",
        highlightthickness=0
    )
    entry_5.place(
        x=429.0,
        y=393.0,
        width=293.0,
        height=35.0
    )
    widgets['entry_bg_5'] = entry_bg_5
    widgets['entry_birthday'] = entry_5

    current_date = datetime.date.today().isoformat()
    entry_image_6 = PhotoImage(
        file=relative_to_assets("entry_6.png"))
    entry_bg_6 = canvas.create_image(
        575.5,
        480.0,
        image=entry_image_6
    )
    entry_6 = Entry(
        bd=0,
        bg="#D9D9D9",
        fg="#000716",
        highlightthickness=0,
    )
    entry_6.insert(tkinter.END, str(current_date))
    entry_6.place(
        x=429.0,
        y=461.0,
        width=293.0,
        height=36.0
    )
    widgets['entry_bg_6'] = entry_bg_6
    widgets['entry_hire_date'] = entry_6

    entry_image_7 = PhotoImage(
        file=relative_to_assets("entry_7.png"))
    entry_bg_7 = canvas.create_image(
        433.5,
        550.0,
        image=entry_image_7
    )
    entry_7 = Entry(
        bd=0,
        bg="#D9D9D9",
        fg="#000716",
        highlightthickness=0
    )
    entry_7.place(
        x=365.0,
        y=531.0,
        width=137.0,
        height=36.0
    )
    widgets['entry_bg_7'] = entry_bg_7
    widgets['entry_login'] = entry_7

    entry_image_8 = PhotoImage(
        file=relative_to_assets("entry_8.png"))
    entry_bg_8 = canvas.create_image(
        598.5,
        550.0,
        image=entry_image_8
    )
    entry_8 = Entry(
        bd=0,
        bg="#D9D9D9",
        fg="#000716",
        highlightthickness=0
    )
    entry_8.place(
        x=530.0,
        y=531.0,
        width=137.0,
        height=36.0
    )
    widgets['entry_bg_8'] = entry_bg_8
    widgets['entry_password'] = entry_8

    t = tkinter.Label(window, text='speciality')
    t.place(x=530.0, y=44.0)
    widgets['label_spec_info'] = t

    button_image_1 = PhotoImage(
        file=relative_to_assets("button_1.png"))
    button_1 = Button(
        image=button_image_1,
        borderwidth=0,
        highlightthickness=0,
        command=employee_info_f,
        relief="flat"
    )
    button_1.place(
        x=14.0,
        y=546.0,
        width=128.0,
        height=45.0
    )
    widgets['button_image_1'] = button_image_1
    widgets['button_1'] = button_1

    button_image_2 = PhotoImage(
        file=relative_to_assets("button_3.png"))
    button_2 = Button(
        image=button_image_2,
        borderwidth=0,
        highlightthickness=0,
        command=fire_employee_f,
        relief="flat"
    )
    button_2.place(
        x=207.0,
        y=546.0,
        width=128.0,
        height=45.0
    )
    widgets['button_image_2'] = button_image_2
    widgets['button_2'] = button_2

    button_image_3 = PhotoImage(
        file=relative_to_assets("button_2.png"))
    button_3 = Button(
        image=button_image_3,
        borderwidth=0,
        highlightthickness=0,
        command=main_menu_f,
        relief="flat"
    )
    button_3.place(
        x=99.0,
        y=12.0,
        width=151.0,
        height=21.0
    )
    widgets['button_image_3'] = button_image_3
    widgets['button_3'] = button_3

    button_image_4 = PhotoImage(
        file=relative_to_assets("button_4.png"))
    button_4 = Button(
        image=button_image_4,
        borderwidth=0,
        highlightthickness=0,
        command=hire_employee_f,
        relief="flat"
    )
    button_4.place(
        x=688.0,
        y=525.0,
        width=88.0,
        height=49.0
    )
    widgets['button_image_4'] = button_image_4
    widgets['button_4'] = button_4

    window.resizable(False, False)

    return window, widgets


def employee_popup_info(fields, values):
    assert len(fields) == len(values)
    
    popup = tkinter.Toplevel()
    popup.title("Данные")

    for i in range(len(fields)):
        label = tkinter.Label(popup, text=f"{fields[i]}: {values[i]}\n")
        label.pack()

    close_button = tkinter.Button(popup, text="Закрыть", command=popup.destroy)
    close_button.pack(pady=10)
