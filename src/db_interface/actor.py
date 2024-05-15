from mysql.connector import Error, errors, errorcode
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk

from .interface import UserInterface
from .gui_screens.actor_roles_menu import actor_roles_menu


class ActorInterface(UserInterface):
    def __init__(self, root, connection, login, db_app):
        super().__init__(root, connection, login, db_app)
        self.widgets = None
        self.main_menu()

    def main_menu(self):

        super().main_menu()

        self.cursor.execute("SELECT get_my_employee_id('"+self.user_login+"')")
        actor_id = self.cursor.fetchall()[0][0]
        print(actor_id)

        self.cursor.execute(
            "SELECT performance_name, performance_date, role_name, type FROM Roles_view "+
            "WHERE actor_id="+str(actor_id)
        )

        role_list = self.cursor.fetchall()
        roles = []
        for role_info in role_list:
            t = [str(s) for s in role_info]
            roles.append(', '.join(t))

        self.root, self.widgets = (
            actor_roles_menu(self.root, self.db_app.auth_stage, roles)
        )

        self.root.mainloop()
