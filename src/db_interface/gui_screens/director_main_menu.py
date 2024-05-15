# This file was generated by the Tkinter Designer by Parth Jadhav
# https://github.com/ParthJadhav/Tkinter-Designer


from pathlib import Path

# from tkinter import *
# Explicit imports to satisfy Flake8
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage
import os


def director_main_menu(window, money_f, login_f, employees_f):
    executable_path = os.path.abspath(__file__)
    executable_directory = os.path.dirname(executable_path)
    widgets = {}

    def relative_to_assets(path: str) -> Path:
        return executable_directory + "/assets/director_main_menu/" + path

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

    canvas.place(x=0, y=0)
    image_image_1 = PhotoImage(
        file=relative_to_assets("image_1.png"))
    image_1 = canvas.create_image(
        200.0,
        300.0,
        image=image_image_1
    )
    widgets['image_image_1'] = image_image_1
    widgets['image_1'] = image_1

    button_image_1 = PhotoImage(
        file=relative_to_assets("button_1.png"))
    button_1 = Button(
        image=button_image_1,
        borderwidth=0,
        highlightthickness=0,
        command=employees_f,
        relief="flat"
    )
    button_1.place(
        x=520.0,
        y=212.0,
        width=174.0,
        height=176.0
    )
    widgets['button_image_1'] = button_image_1
    widgets['button_1'] = button_1

    button_image_2 = PhotoImage(
        file=relative_to_assets("button_2.png"))
    button_2 = Button(
        image=button_image_2,
        borderwidth=0,
        highlightthickness=0,
        command=money_f,
        relief="flat"
    )
    button_2.place(
        x=113.0,
        y=212.0,
        width=174.0,
        height=176.0
    )
    widgets['button_image_2'] = button_image_2
    widgets['button_2'] = button_2

    button_image_3 = PhotoImage(
        file=relative_to_assets("button_3.png"))
    button_3 = Button(
        image=button_image_3,
        borderwidth=0,
        highlightthickness=0,
        command=login_f,
        relief="flat"
    )
    button_3.place(
        x=19.0,
        y=22.0,
        width=124.0,
        height=54.0
    )
    widgets['button_image_3'] = button_image_3
    widgets['button_3'] = button_3

    window.resizable(False, False)

    return window, widgets
