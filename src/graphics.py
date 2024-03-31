import tkinter as tk
from mysql.connector import connect, Error
from tkinter import messagebox
from datetime import datetime

from config import config


class DatabaseApp:
    def __init__(self):
        self.root = tk.Tk()
        self.connection = None
        self.cursor = None

        self.root.title("Информационная система театра")
        self.root.geometry("800x600")
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

        tk.Label(self.root, text="Авторизация").pack()

        tk.Label(self.root, text="Имя хоста базы данных:").pack()
        self.host_entry = tk.Entry(self.root)
        self.host_entry.insert(0, config['host'])
        self.host_entry.pack()

        tk.Label(self.root, text="Логин:").pack()
        self.login_entry = tk.Entry(self.root)
        self.login_entry.pack()

        tk.Label(self.root, text="Пароль:").pack()
        self.password_entry = tk.Entry(self.root, show='*')
        self.password_entry.pack()

        tk.Button(self.root, text="Вход", command=self.auth_to_database).pack()

        self.root.mainloop()

    def auth_to_database(self):
        host = self.host_entry.get()
        login = self.login_entry.get()
        password = self.password_entry.get()

        try:
            # self.connection = connect(host=host, user=login, password=password)
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
        def get_repertoire_income():
            try:
                self.cursor.execute("select get_current_repertoire_income()")
                data = self.cursor.fetchall()
                messagebox.showinfo(title="Доход", message=data)
            except Error as e:
                messagebox.showerror("Ошибка", e.msg)

        def get_performance_info():
            def search():
                try:
                    self.cursor.execute("call show_available_tickets("+id_entry.get()+")")
                    show = self.cursor.fetchall()
                    show = show[0]
                    self.cursor.nextset()
                    prices = self.cursor.fetchall()

                    pp = tk.Toplevel(self.root)
                    pp.title("Информация о выступлении")
                    pp.geometry("800x300")
                    tk.Label(pp, text="Спектакль: \""+show[0]+"\"").grid(row=0, column=0)
                    tk.Label(pp, text="Дата: \""+show[1].strftime("%d/%m/%Y")+"\"").grid(row=1, column=0)
                    tk.Label(pp, text="Автор: \""+show[2]+"\"").grid(row=2, column=0)
                    tk.Label(pp, text="Жанр: \""+show[3]+"\"").grid(row=3, column=0)
                    tk.Label(pp, text="Место:").grid(row=4, column=0)
                    tk.Label(pp, text="Цена:").grid(row=4, column=1)
                    tk.Label(pp, text="Всего билетов:").grid(row=4, column=2)
                    tk.Label(pp, text="Свободно билетов:").grid(row=4, column=3)

                    for m in range(len(prices)):
                        for k in range(0, len(prices[m])):
                            tk.Label(pp, text=prices[m][k]).grid(row=5+m, column=k)

                    try:
                        self.cursor.nextset()  # иначе пишет command out of sync, не понимаю почему
                    except Error:
                        pass
                except Error as e:
                    messagebox.showerror("Ошибка", e.msg)

            popup = tk.Toplevel(self.root)
            popup.title("Информация о выступлении")
            popup.geometry("400x200")
            tk.Label(popup, text="Введите ИД интересующего выступления").pack()
            id_entry = tk.Entry(popup)
            id_entry.pack()
            tk.Button(popup, text="Поиск", command=search).pack()
            tk.Button(popup, text="Выход", command=popup.destroy).pack()

        self.clear_window()
        (tk.Label(self.root, text="Выберите таблицу для взаимодействия")
         .grid(row=0, column=1, padx=5, pady=5))

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
            .grid(row=N_ROWS+1, column=0))
        (tk.Button(self.root, text="Доход за текущий сезон", command=get_repertoire_income)
            .grid(row=N_ROWS+2, column=0))
        (tk.Button(self.root, text="Получить информацию о выступлении", command=get_performance_info)
         .grid(row=N_ROWS+2, column=1))

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
