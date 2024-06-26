# This file was generated by the Tkinter Designer by Parth Jadhav
# https://github.com/ParthJadhav/Tkinter-Designer
import tkinter
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
        return executable_directory+"/assets/login_menu/"+path

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
        231.0,
        image=image_image_1
    )
    widgets['image_image_1'] = image_image_1
    widgets['image_1'] = image_1

    image_image_2 = PhotoImage(
        file=relative_to_assets("image_2.png"))
    image_2 = canvas.create_image(
        248.0,
        300.0,
        image=image_image_2
    )
    widgets['image_image_2'] = image_image_2
    widgets['image_2'] = image_2

    entry_1 = tkinter.Entry()
    entry_1.place(
        x = 545.0,
        y = 115.0,
        width = 230.0,
        height = 29.0
    )

    widgets['entry_1'] = entry_1

    entry_2 = tkinter.Entry()
    entry_2.place(
        x = 545.0,
        y = 205.0,
        width = 230.0,
        height = 29.0
    )
    widgets['entry_2'] = entry_2

    entry_3 = tkinter.Entry()
    entry_3.place(
        x=544.0,
        y=307.0,
        width=230.0,
        height=29.0
    )
    widgets['entry_3'] = entry_3

    entry_4 = tkinter.Entry(show="*")
    entry_4.place(
        x=544.0,
        y=394.0,
        width=230.0,
        height=29.0
    )
    widgets['entry_4'] = entry_4

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
        x=547.0,
        y=468.0,
        width=223.0,
        height=93.0
    )
    widgets['button_image_1'] = button_image_1
    widgets['button_1'] = button_1

    entry_1.insert(tkinter.END, 'localhost')
    entry_2.insert(tkinter.END, '3306')


    window.resizable(False, False)

    widgets['canvas'] = canvas

    return window, widgets

