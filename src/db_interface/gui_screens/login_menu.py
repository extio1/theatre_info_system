# This file was generated by the Tkinter Designer by Parth Jadhav
# https://github.com/ParthJadhav/Tkinter-Designer


from pathlib import Path

# from tkinter import *
# Explicit imports to satisfy Flake8
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage
import os


def login_menu(window, login_button_f):
    executable_path = os.path.abspath(__file__)
    executable_directory = os.path.dirname(executable_path)
    widgets = {}

    def relative_to_assets(path: str) -> str:
        return executable_directory+"/assets/frame0/"+path

    window.geometry("800x600")
    window.configure(bg="#FFFFFF")

    canvas = Canvas(
        window,
        bg="#FFFFFF",
        height=600,
        width=800,
        bd=0,
        highlightthickness=0,
        relief="ridge"
    )

    canvas.place(x=0, y=0)
    canvas.create_rectangle(
        496.0,
        0.0,
        800.0,
        600.0,
        fill="#D9D9D9",
        outline="")

    image_image_1 = PhotoImage(
        file=relative_to_assets("image_1.png"))
    image_1 = canvas.create_image(
        663.0,
        194.0,
        image=image_image_1
    )
    widgets['image_1'] = image_image_1

    image_image_2 = PhotoImage(
        file=relative_to_assets("image_2.png"))
    image_2 = canvas.create_image(
        248.0,
        300.0,
        image=image_image_2
    )
    widgets['image_2'] = image_image_2

    entry_image_1 = PhotoImage(
        file=relative_to_assets("entry_1.png"))
    entry_bg_1 = canvas.create_image(
        660.0,
        239.5,
        image=entry_image_1
    )
    widgets['entry_bg_1'] = entry_image_1

    entry_1 = Entry(
        bd=0,
        bg="#FFFFFF",
        fg="#000716",
        highlightthickness=0
    )
    entry_1.place(
        x=545.0,
        y=224.0,
        width=230.0,
        height=29.0
    )
    widgets['entry_1'] = entry_1

    entry_image_2 = PhotoImage(
        file=relative_to_assets("entry_2.png"))
    entry_bg_2 = canvas.create_image(
        660.0,
        132.5,
        image=entry_image_2
    )
    widgets['entry_image_2'] = entry_image_2

    entry_2 = Entry(
        bd=0,
        bg="#FFFFFF",
        fg="#000716",
        highlightthickness=0
    )
    entry_2.insert(0, "localhost")
    entry_2.place(
        x=545.0,
        y=117.0,
        width=230.0,
        height=29.0
    )
    widgets['entry_2'] = entry_2

    entry_image_3 = PhotoImage(
        file=relative_to_assets("entry_3.png"))
    entry_bg_3 = canvas.create_image(
        659.0,
        346.5,
        image=entry_image_3
    )
    widgets['entry_image_3'] = entry_image_3

    entry_3 = Entry(
        show="*"
    )
    entry_3.place(
        x=544.0,
        y=331.0,
        width=230.0,
        height=29.0
    )
    widgets['entry_3'] = entry_3

    button_image_1 = PhotoImage(
        file=relative_to_assets("button_1.png"))
    button_1 = Button(
        image=button_image_1,
        borderwidth=0,
        highlightthickness=0,
        command=login_button_f,
        relief="flat"
    )
    button_1.place(
        x=544.0,
        y=449.0,
        width=223.0,
        height=93.0
    )
    widgets['button_1'] = button_image_1

    window.resizable(False, False)

    widgets['canvas'] = canvas

    return window, widgets

