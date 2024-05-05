import tkinter as tk
from mysql.connector import connect, Error
from tkinter import messagebox

from config import config
from db_interface.gui_screens.login_menu import login_menu
from db_interface.client import VisitorInterface
from db_interface.director import DirectorInterface
from db_interface.admin import AdministratorInterface


view_class = {'`client`@`%`': VisitorInterface,
              '`director`@`%`': DirectorInterface
              }


class DatabaseApp:
    def __init__(self):
        self.cursor = None
        self.user_interface = None
        self.root = tk.Tk()
        self.connection = None

        self.auth_stage()

    def auth_stage(self):
        self.root, widgets = login_menu(self.root, self.auth_to_database)
        self.login_entry = widgets['entry_1']
        self.host_entry = widgets['entry_2']
        self.password_entry = widgets['entry_3']

        self.root.mainloop()

    def auth_to_database(self):
        host = self.host_entry.get()
        login = self.login_entry.get()
        password = self.password_entry.get()

        try:
            self.connection = connect(host=host, user=login, password=password)
            self.cursor = self.connection.cursor()
            self.cursor.execute("USE " + config["database"])
        except Error as e:
            messagebox.showerror("Ошибка во время авторизации", e.msg)

        self.create_view(login)

    def create_view(self, login):
        if login == 'root':
            AdministratorInterface(self.root, self.connection, self)
        else:
            try:
                self.cursor = self.connection.cursor()
                self.cursor.execute("SELECT CURRENT_ROLE()")

                view_class[self.cursor.fetchall()[0][0]](self.root, self.connection, self)
            except Error as e:
                messagebox.showerror("Ошибка во время авторизации", e.msg)

    def on_closing(self):
        if tk.messagebox.askokcancel("Выход", "Вы уверены, что хотите выйти?"):
            try:
                self.connection.close()
            except Error as e:
                print("Ошибка разрыва соединения", e.msg)

            self.root.destroy()


def main():
    DatabaseApp()


if __name__ == "__main__":
    main()
