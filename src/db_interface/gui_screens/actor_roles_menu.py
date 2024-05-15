# This file was generated by the Tkinter Designer by Parth Jadhav
# https://github.com/ParthJadhav/Tkinter-Designer
import tkinter
from pathlib import Path

# from tkinter import *
# Explicit imports to satisfy Flake8
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage
import os


def actor_roles_menu(window, login_f, role_list):
    executable_path = os.path.abspath(__file__)
    executable_directory = os.path.dirname(executable_path)
    widgets = {}

    def relative_to_assets(path: str) -> Path:
        return executable_directory + "/assets/actor_roles_menu/" + path

    window.geometry("800x600")
    window.configure(bg="#892727")

    canvas = Canvas(
        window,
        bg="#892727",
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
        74.0,
        300.0,
        image=image_image_1
    )
    widgets['image_image_1'] = image_image_1
    widgets['image_1'] = image_1

    listbox = tkinter.Listbox(canvas)
    listbox.bind('<<ListboxSelect>>', None)
    listbox.place(x=196, y=164, width=545, height=393)
    for e in role_list:
        listbox.insert(tkinter.END, str(e))

    widgets['listbox_roles'] = listbox

    canvas.create_rectangle(
        196.0,
        164.0,
        741.0,
        557.0,
        fill="#000000",
        outline="")

    canvas.create_text(
        360.0,
        70.0,
        anchor="nw",
        text="Мои роли",
        fill="#FFFFFF",
        font=("Inder Regular", 40 * -1)
    )

    button_image_1 = PhotoImage(
        file=relative_to_assets("button_1.png"))
    button_1 = Button(
        image=button_image_1,
        borderwidth=0,
        highlightthickness=0,
        command=login_f,
        relief="flat"
    )
    button_1.place(
        x=13.0,
        y=22.0,
        width=124.0,
        height=54.0
    )
    widgets['button_1'] = button_1
    widgets['button_image_1'] = button_image_1

    window.resizable(False, False)

    return window, widgets