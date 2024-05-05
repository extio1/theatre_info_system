from mysql.connector import Error, errors, errorcode
import tkinter as tk
from tkinter import messagebox

from .interface import UserInterface
from config import config


class AdministratorInterface(UserInterface):
    def __init__(self, root, connection, db_app):
        super().__init__(root, connection, db_app)
        self.root.resizable(True, True)
        self.MIGRATE_SCRIPT_PATH = "script/migrate/migrate.sql"
        self.SAMPLE_SCRIPT_PATH = "script/sample/1.sql"

    def main_menu(self):
        def migrate():
            from mysql.connector import Error
            try:
                with self.connection.cursor() as cursor:
                    cursor.execute("DROP DATABASE IF EXISTS " + config["database"])
                    cursor.execute("CREATE DATABASE " + config["database"])
                    cursor.execute("USE " + config["database"])

                    with open(self.MIGRATE_SCRIPT_PATH, "r") as f:
                        for create_table_query in f.read().split('//'):
                            print(create_table_query)
                            if len(create_table_query) > len("CREATE"):
                                cursor.execute(create_table_query)
                                self.connection.commit()

                messagebox.showinfo(title="Success", message="Success")
            except Error as e:
                messagebox.showerror(message=e.msg)

        def fill():
            from mysql.connector import Error
            try:
                with self.connection.cursor() as cursor:
                    with open(self.SAMPLE_SCRIPT_PATH, "r") as f:
                        for insert_table_query in f.read().split('//'):
                            if len(insert_table_query) > len("INSERT"):
                                print(insert_table_query)
                                cursor.execute(insert_table_query)
                        self.connection.commit()

                    messagebox.showinfo(title="Success", message="Success")
            except Error as e:
                messagebox.showerror(message=e.msg)

        super().main_menu()

        (tk.Label(self.root, text="Выберите таблицу для взаимодействия")
         .grid(row=0, column=1, padx=5, pady=5))
        (tk.Button(self.root, text="Вернутся на страницу авторизации", command=self.db_app.auth_stage)
         .grid(row=0, column=0, padx=5, pady=5))

        self.cursor.execute("SHOW tables")
        tables = []

        for table in self.cursor:
            tables.append(table)

        N_COLS = 3
        N_ROWS = len(tables) // N_COLS + 1
        for i in range(len(tables)):
            (tk.Button(self.root, text=tables[i], command=lambda name=tables[i][0]: self.table_menu(name))
             .grid(row=i // N_COLS + 1, column=i % N_COLS, padx=5, pady=5))

        (tk.Label(self.root, text="Функции и процедуры")
         .grid(row=N_ROWS + 1, column=0))
        (tk.Label(self.root, text="Управление базой данных")
         .grid(row=N_ROWS + 3, column=0))
        (tk.Button(self.root, text="Удалить всё и выполнить миграцию", command=migrate)
         .grid(row=N_ROWS + 4, column=0))
        (tk.Button(self.root, text="Заполнить тестовыми данными", command=fill)
         .grid(row=N_ROWS + 4, column=1))

    def table_menu(self, table_name):
        def refresh_table_data():
            try:
                self.cursor.execute("SELECT * FROM " + table_name)
                rows = self.cursor.fetchall()
                data_listbox.delete(0, tk.END)
                for row in rows:
                    data_listbox.insert(tk.END, row)
            except Error as er:
                messagebox.showerror("Ошибка во время запроса данных с сервера БД", er.msg)

        def delete_table_data():
            try:
                indexes = data_listbox.curselection()
                for i in indexes:
                    pk = str(data_listbox.get(i)[0])
                    query = "DELETE FROM " + table_name + " WHERE " + table_info[0][0] + "=" + pk
                    print(query)
                    self.cursor.execute(query)
                    self.connection.commit()
                refresh_table_data()
            except Error as er:
                messagebox.showerror("Ошибка во время удаления строки с сервера БД", er.msg)

        def add_table_data():
            try:
                query = "INSERT INTO " + table_name + " VALUES ("
                for ent in entries:
                    query += ent.get() + ", "
                query = query[:-2]
                query += ")"

                print(query)
                self.cursor.execute(query)
                self.connection.commit()
                refresh_table_data()
            except Error as er:
                messagebox.showerror("Ошибка во время добавления строки на сервер БД", er.msg)

        self.clear_window()

        try:
            self.cursor.execute("SHOW COLUMNS FROM " + table_name)
            table_info = self.cursor.fetchall()
            table_info_str = ""
            for col in table_info:
                table_info_str += col[0] + "; "

            (tk.Button(self.root, text="В главное меню", command=self.main_menu)
             .grid(row=0, column=2, sticky='e'))
            (tk.Label(self.root, text=table_name + ": " + table_info_str)
             .grid(row=0, column=0))
            (tk.Button(self.root, text="Просмотреть данные", command=refresh_table_data)
             .grid(row=1, column=0))
            (tk.Button(self.root, text="Удалить выделенные строки", command=delete_table_data)
             .grid(row=2, column=0))
            data_listbox = tk.Listbox(self.root, width=30, height=20)
            data_listbox.grid(row=3, column=0, rowspan=10)

            (tk.Label(self.root, text="Добавление данных")
             .grid(row=1, column=1, columnspan=2, ipady=1))
            (tk.Button(self.root, text="Добавить запись", command=add_table_data)
             .grid(row=2, column=1, columnspan=2))

            entries = []
            for i in range(len(table_info)):
                (tk.Label(self.root, text=table_info[i][0] + ":")
                 .grid(row=3 + i, column=1))
                entry = tk.Entry(self.root)
                entry.grid(row=3 + i, column=2, sticky='e')
                entries.append(entry)

        except Error as e:
            messagebox.showerror("Ошибка", e.msg)