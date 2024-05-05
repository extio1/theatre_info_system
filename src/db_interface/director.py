from mysql.connector import Error
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import datetime

from .interface import UserInterface


class DirectorInterface(UserInterface):
    def __init__(self, root, connection, db_app):
        super().__init__(root, connection, db_app)
        self.entries = None
        self.employee_tree = None
        self.refresh_gui_item = []
        self.employee_view = {'Рабочий': 'Workers_private_view',
                              'Продюссер': 'Producers_private_view',
                              'Актёр': 'Actors_private_view',
                              'Музыкант': 'Musicians_private_view',
                              }

        self.employee_entries = {
            'Рабочий': ['ФИО (отчество, если есть)*', 'Зарплата*', 'Дата начала работы*', 'День рождения*'],
            'Продюссер': ['ФИО (отчество, если есть)*', 'Зарплата*', 'Дата начала работы*', 'День рождения*'],
            'Музыкант': ['ФИО (отчество, если есть)*', 'Зарплата*', 'Дата начала работы*', 'День рождения*'],
            'Актёр': ['ФИО (отчество, если есть)*', 'Зарплата*', 'Дата начала работы*', 'День рождения*',
                      'Рост*', 'Вес*', 'Тембр голоса*', 'Пол*', 'Национальность']
        }

    def main_menu(self):
        def get_repertoire_income():
            try:
                self.cursor.execute("select get_current_repertoire_income()")
                data = self.cursor.fetchall()
                messagebox.showinfo(title="Доход", message=data)
            except Error as e:
                messagebox.showerror("Ошибка", e.msg)

        def employees_menu():
            def fire_employee():
                yes = messagebox.askyesno(title="Увольнение",
                                          message="Вы действительно хотите уволить " +
                                                  str(self.employee_tree.item(self.employee_tree.selection())['values'][
                                                          0]) + "?"
                                          )

                if yes:
                    try:
                        e_id = self.employee_tree.item(self.employee_tree.selection())['values'][-1]
                        self.cursor.execute("DELETE FROM Employees WHERE id=" + str(e_id))
                        self.connection.commit()
                        refresh_employee_tree(None)
                    except Error as e:
                        messagebox.showerror("Ошибка", e.msg)

            def hire_employee():
                try:
                    self.cursor.callproc(
                        "InsertInto" + self.employee_view[employee_box.get()],
                        [e.get() for e in self.entries]
                    )
                    self.connection.commit()
                    refresh_employee_tree(None)
                except Error as e:
                    messagebox.showerror("Ошибка", e.msg)

            def refresh_employee_tree(event):
                def add_refreshable_item(item, row, col):
                    item.grid(row=row, column=col)
                    self.refresh_gui_item.append(item)
                    return item

                if len(self.refresh_gui_item):
                    for i in self.refresh_gui_item:
                        i.destroy()

                employee_type = employee_box.get()
                self.cursor.execute("SHOW COLUMNS FROM " + self.employee_view[employee_type])
                view_columns = self.cursor.fetchall()
                self.employee_tree = ttk.Treeview(self.root, columns=[c[0] for c in view_columns], show="headings")
                self.refresh_gui_item.append(self.employee_tree)

                for c in view_columns:
                    self.employee_tree.heading(c[0], text=c[0])
                self.employee_tree.grid(row=2, column=0, columnspan=len(view_columns))

                self.cursor.execute("SELECT * FROM " + self.employee_view[employee_type])
                data_employees = self.cursor.fetchall()
                for row in data_employees:
                    self.employee_tree.insert("", "end", values=row)

                self.entries = []
                ROW = 3
                add_refreshable_item(tk.Label(self.root, text='Нанять ' + employee_type), ROW, 0)

                entries_text = self.employee_entries[employee_type]
                for i in range(len(entries_text)):
                    add_refreshable_item(tk.Label(self.root, text=entries_text[i]), ROW + i + 1, 0)
                    entry = add_refreshable_item(tk.Entry(self.root), ROW + i + 2, 0)
                    self.entries.append(entry)
                    ROW += 2

                    if entries_text[i] == 'Дата начала работы*':
                        entry.insert(0, str(datetime.date.today()))

                add_refreshable_item(tk.Button(self.root, text='Нанять', command=hire_employee),
                                     ROW + len(view_columns) + 1, 0)
                add_refreshable_item(tk.Button(self.root, text='Уволить', command=fire_employee), 3, 2)

            self.clear_window()
            (tk.Button(self.root, text="В главное меню", command=self.main_menu)
             .grid(row=0, column=3))

            employee_box = ttk.Combobox(self.root, values=list(self.employee_view.keys()))
            employee_box.bind("<<ComboboxSelected>>", refresh_employee_tree)
            employee_box.grid(row=1, column=0)

        super().main_menu()

        (tk.Button(self.root, text="Доход за текущий сезон", command=get_repertoire_income)
         .grid(row=1, column=1))

        (tk.Button(self.root, text="Меню управления подчиненными", command=employees_menu)
         .grid(row=2, column=1))