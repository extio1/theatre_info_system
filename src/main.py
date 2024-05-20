import tkinter as tk
from mysql.connector import connect, Error
from tkinter import messagebox

from config import config
from db_interface.gui_screens.login_menu import login_menu
from db_interface.client import VisitorInterface
from db_interface.director import DirectorInterface
from db_interface.admin import AdministratorInterface
from db_interface.actor import ActorInterface

role_interface = {'`client`@`%`': VisitorInterface,
                  '`director`@`%`': DirectorInterface,
                  '`actor`@`%`': ActorInterface
                  }


class DatabaseApp:
    def __init__(self):
        self.port_entry = None
        self.password_entry = None
        self.host_entry = None
        self.login_entry = None
        self.cursor = None
        self.user_interface = None
        self.root = tk.Tk()
        self.connection = None

        self.auth_stage()

    def auth_stage(self):
        self.root, widgets = login_menu(self.root, self.auth_to_database)
        self.host_entry = widgets['entry_1']
        self.port_entry = widgets['entry_2']
        self.login_entry = widgets['entry_3']
        self.password_entry = widgets['entry_4']

        self.root.mainloop()

    def auth_to_database(self):
        host = self.host_entry.get()
        port = int(self.port_entry.get())
        login = self.login_entry.get()
        password = self.password_entry.get()

        if self.connection and self.connection.is_connected():
            self.connection.close()

        try:
            self.connection = connect(host=host, port=port, user=login, password=password)
            self.create_view(login)
        except Error as e:
            messagebox.showerror("Ошибка во время авторизации", e.msg)

    def create_view(self, login):
        self.cursor = self.connection.cursor()
        self.cursor.execute("USE " + config['database'])

        if login == 'root':
            AdministratorInterface(self.root, self.connection, login, self)
        else:
            try:
                self.cursor.execute("SELECT CURRENT_ROLE()")
                current_role = self.cursor.fetchall()[0][0]

                role_interface[current_role](self.root, self.connection, login, self)
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
