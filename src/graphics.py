import tkinter as tk
from mysql.connector import connect, Error
from tkinter import ttk
from tkinter import messagebox

from config import config


class DatabaseApp:
    def __init__(self):
        self.root = tk.Tk()
        self.connection = None
        self.cursor = None

        self.root.title("Информационная система театра")
        self.root.geometry("800x600")
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

        self.label = tk.Label(self.root, text="Авторизация")
        self.label.pack()

        self.host_label = tk.Label(self.root, text="Имя хоста базы данных:")
        self.host_label.pack()
        self.host_entry = tk.Entry(self.root)
        self.host_entry.insert(0, config['host'])
        self.host_entry.pack()

        self.login_label = tk.Label(self.root, text="Логин:")
        self.login_label.pack()
        self.login_entry = tk.Entry(self.root)
        self.login_entry.pack()

        self.password_label = tk.Label(self.root, text="Пароль:")
        self.password_label.pack()
        self.password_entry = tk.Entry(self.root)
        self.password_entry.pack()

        self.submit_button = tk.Button(self.root, text="Вход", command=self.auth_to_database)
        self.submit_button.pack()

        self.root.mainloop()

    def auth_to_database(self):
        host = self.host_entry.get()
        login = self.login_entry.get()
        password = self.password_entry.get()
        # !!!!!!!!!!!!!!!!!!!!!!!! ВЕРНУТЬ НОРМАЛЬНЫЕ ПАРАМЕНТЫ ДЛЯ ПОДКЛЮЧЕНИЯ
        try:
            self.connection = connect(host=host, user='root', password='123321')
            self.cursor = self.connection.cursor()
            self.cursor.execute("USE " + config["database"])

            self.show_main_menu()
        except Error as e:
            messagebox.showerror("Ошибка во время авторизации", e.msg)

    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def on_closing(self):
        if tk.messagebox.askokcancel("Выход", "Вы уверены, что хотите выйти?"):
            try:
                self.connection.close()
            except Error as e:
                print("Ошибка разрыва соединения", e.msg)

            self.root.destroy()

    def show_main_menu(self):
        self.clear_window()
        (tk.Label(self.root, text="Выберите таблицу для взаимодействия")
         .grid(row=0, column=1, padx=5, pady=5))

        self.cursor.execute("SHOW tables")
        tables = []

        for table in self.cursor:
            tables.append(table)

        N_COLS = 3
        for i in range(len(tables)):
            (tk.Button(self.root, text=tables[i], command=lambda name=tables[i][0]: self.table_menu(name))
                .grid(row=i // N_COLS + 1, column=i % N_COLS, padx=5, pady=5))

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
                    query = "DELETE FROM "+table_name+" WHERE "+table_info[0][0]+"="+pk
                    print(query)
                    self.cursor.execute(query)
                    self.connection.commit()
                refresh_table_data()
            except Error as er:
                messagebox.showerror("Ошибка во время удаления строки с сервера БД", er.msg)

        def add_table_data():
            try:
                query = "INSERT INTO "+table_name+" VALUES ("
                for ent in entries:
                    query += ent.get()+", "
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
            self.cursor.execute("SHOW COLUMNS FROM "+table_name)
            table_info = self.cursor.fetchall()
            table_info_str = ""
            for col in table_info:
                table_info_str += col[0]+"; "

            (tk.Button(self.root, text="В главное меню", command=self.show_main_menu)
                .grid(row=0, column=2, sticky='e'))
            (tk.Label(self.root, text=table_name+": "+table_info_str)
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
                (tk.Label(self.root, text=table_info[i][0]+":")
                    .grid(row=3+i, column=1))
                entry = tk.Entry(self.root)
                entry.grid(row=3+i, column=2, sticky='e')
                entries.append(entry)

        except Error as e:
            messagebox.showerror("Ошибка", e.msg)


def main():
    DatabaseApp()


if __name__ == "__main__":
    main()
