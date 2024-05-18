from mysql.connector import Error
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import datetime

from .interface import UserInterface
from .gui_screens.director_main_menu import director_main_menu
from .gui_screens.director_employees_menu import director_employees_menu, employee_popup_info


class DirectorInterface(UserInterface):
    def __init__(self, root, connection, login, db_app):
        super().__init__(root, connection, login, db_app)
        self.entries = None
        self.employee_tree = None
        self.refresh_gui_item = []
        self.widgets = None

        self.employee_view = {
            'Рабочий': 'Workers_private_view',
            'Продюссер': 'Producers_private_view',
            'Актёр': 'Actors_private_view',
            'Музыкант': 'Musicians_private_view'
        }

        self.employee_role = {
            'Рабочий': 'worker',
            'Продюссер': 'producer',
            'Актёр': 'actor',
            'Музыкант': 'musician'
        }

        self.employees = []
        self.current_employee = None
        self.curr_employee_type = None

        self.main_menu()

    def main_menu(self):
        def get_repertoire_income():
            try:
                self.connection.commit()
                self.cursor.execute("select get_current_repertoire_income()")
                data = self.cursor.fetchall()
                messagebox.showinfo(title="Доход", message=data)
            except Error as e:
                messagebox.showerror("Ошибка", e.msg)

        def employees_menu():
            def fire_employee():
                employee_fullname = str(self.current_employee[1])
                employee_id = str(self.current_employee[0])
                yes = messagebox.askyesno(title="Увольнение",
                                          message="Вы действительно хотите уволить " + employee_fullname + "?"
                                          )
                if yes:
                    try:
                        self.cursor.execute("DELETE FROM Employees WHERE id=" + employee_id)
                        self.connection.commit()
                        employees_menu()
                    except Error as e:
                        messagebox.showerror("Ошибка", e.msg)

            def hire_employee():
                name = self.widgets['entry_name'].get()
                surname = self.widgets['entry_surname'].get()
                patronymic = self.widgets['entry_patronymic'].get()
                salary = self.widgets['entry_salary'].get()
                birthday = self.widgets['entry_birthday'].get()
                hire_date = self.widgets['entry_hire_date'].get()
                login = self.widgets['entry_login'].get()
                password = self.widgets['entry_password'].get()

                try:
                    self.cursor.callproc(
                        "InsertInto" + self.employee_view[self.curr_employee_type],
                        [name, surname, patronymic, salary, birthday, hire_date]
                    )

                    if login:  # if director wants to create user for employee
                        self.cursor.execute(
                            "SELECT LAST_INSERT_ID()"
                        )

                        id_inserted = str(self.cursor.fetchall()[0][0])

                        self.cursor.execute(
                            "CREATE USER IF NOT EXISTS '" + login + "'@'%' IDENTIFIED BY '"
                            + password + "' DEFAULT ROLE '" + self.employee_role[self.curr_employee_type] + "'"
                        )

                        self.cursor.execute(
                            "INSERT INTO Employee_login(employee_id, login) VALUES (" +
                            id_inserted + ", '" + login + "')"
                        )

                    self.connection.commit()

                    employees_menu()
                except Error as e:
                    messagebox.showerror("Ошибка", e.msg)

            def employee_info():
                # if any entity from list was chosen
                if self.current_employee[0]:
                    self.cursor.execute("SHOW COLUMNS FROM " +
                                        self.employee_view[self.curr_employee_type])
                    features = [a[0] for a in self.cursor.fetchall()]

                    self.cursor.execute("SELECT * FROM " +
                                        self.employee_view[self.curr_employee_type] +
                                        " WHERE id=" + str(self.current_employee[0]))

                    info = self.cursor.fetchall()[0]

                    employee_popup_info(features, info)

            def refresh_employee_list(a):
                self.curr_employee_type = self.widgets['combo_box_employee'].get()
                self.widgets['label_spec_info']['text'] = self.curr_employee_type
                self.cursor.execute("SELECT DISTINCT id, name FROM " +
                                    self.employee_view[self.curr_employee_type])
                self.employees = self.cursor.fetchall()

                self.widgets['listbox_employees'].delete(0, tk.END)
                for e in self.employees:
                    self.widgets['listbox_employees'].insert(tk.END, str(e[0]) + " " + str(e[1]))

            def refresh_curr_employee(a):
                if self.widgets['listbox_employees'].curselection():
                    selected_index = self.widgets['listbox_employees'].curselection()[0]
                    self.current_employee = self.employees[selected_index]

            self.clear_window()

            self.root, self.widgets = (
                director_employees_menu(self.root,
                                        main_menu_f=self.main_menu,
                                        employee_info_f=employee_info,
                                        fire_employee_f=fire_employee,
                                        hire_employee_f=hire_employee,
                                        employee_list_on_select_f=refresh_curr_employee,
                                        employee_types=list(self.employee_view.keys()),
                                        employee_types_on_select_f=refresh_employee_list
                                        )
            )

        super().main_menu()

        self.root, self.widgets = (
            director_main_menu(self.root,
                               money_f=get_repertoire_income,
                               employees_f=employees_menu,
                               login_f=self.db_app.auth_stage,
                               )
        )

        self.root.mainloop()
