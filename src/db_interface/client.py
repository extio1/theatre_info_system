from mysql.connector import Error, errors, errorcode
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk

from .interface import UserInterface


class VisitorInterface(UserInterface):
    def __init__(self, root, connection, db_app):
        super().__init__(root, connection, db_app)
        self.employee_view = {'Продюссер': 'Producers_public_view',
                              'Актёр': 'Actors_public_view',
                              'Музыкант': 'Musicians_public_view',
                              }
        self.employee_tree = None

    def main_menu(self):
        def get_performance_info():
            def refresh_info(pp):
                for widget in pp.winfo_children():
                    widget.destroy()

                selected_show = shows[show_combobox.current()]

                self.cursor.execute("call show_available_tickets(" + str(selected_show[0]) + ")")
                prices = self.cursor.fetchall()

                pp.title("Информация о выступлении")
                pp.geometry("800x300")
                tk.Label(pp, text="Спектакль: \"" + selected_show[1] + "\"").grid(row=0, column=0)
                tk.Label(pp, text="Дата: \"" + selected_show[2].strftime("%d/%m/%Y") + "\"").grid(row=1, column=0)
                tk.Label(pp, text="Автор: \"" + selected_show[3] + "\"").grid(row=2, column=0)
                tk.Label(pp, text="Жанр: \"" + selected_show[4] + "\"").grid(row=3, column=0)
                tk.Label(pp, text="Место:").grid(row=4, column=0)
                tk.Label(pp, text="Цена:").grid(row=4, column=1)
                tk.Label(pp, text="Всего билетов:").grid(row=4, column=2)
                tk.Label(pp, text="Свободно билетов:").grid(row=4, column=3)

                place_box = ttk.Combobox(pp, values=[p[0] for p in prices])
                place_box.grid(row=5 + len(prices), column=1)
                amount_entry = tk.Entry(pp)
                amount_entry.grid(row=5 + len(prices), column=2)

                (tk.Button(
                    pp,
                    text='Купить',
                    command=lambda p=place_box, a=amount_entry: buy_ticket(pp, selected_show[0], p, a)
                ).grid(row=5 + len(prices), column=0))

                for m in range(len(prices)):
                    for k in range(0, len(prices[m])):
                        tk.Label(pp, text=prices[m][k]).grid(row=5 + m, column=k)

                try:
                    self.cursor.nextset()  # иначе command out of sync
                except Error:
                    pass

            def buy_ticket(pp, show_id, place_box, amount_entry):
                try:
                    self.cursor.callproc('buy_ticket', [show_id, place_box.get(), amount_entry.get()])
                    messagebox.showinfo("Покупка", "Операция прошла успешно", parent=pp)
                    self.connection.commit()
                    refresh_info(pp)
                except errors.DatabaseError as err:
                    if err.errno == errorcode.ER_SIGNAL_EXCEPTION:
                        messagebox.showerror("Ошибка",
                                             "Произошла ошибка:" + str(err),
                                             parent=pp)

            def search():
                try:
                    pp = tk.Toplevel(self.root)
                    pp.geometry("800x300")
                    refresh_info(pp)
                except Error as e:
                    messagebox.showerror("Ошибка", e.msg, parent=pp)

            popup = tk.Toplevel(self.root)
            popup.title("Информация о выступлении")
            popup.geometry("400x200")

            tk.Label(popup, text="Выберите название интерусующего выступления:").pack()
            self.cursor.execute("SELECT * FROM Repertoire_info_view")
            shows = self.cursor.fetchall()
            show_combobox = ttk.Combobox(popup, values=[show[1] for show in shows])
            show_combobox.pack()

            tk.Button(popup, text="Поиск", command=search).pack()
            tk.Button(popup, text="Выход", command=popup.destroy).pack()

        def get_employees_info():
            def refresh_employee_tree(e):
                if self.employee_tree:
                    self.employee_tree.destroy()

                employee_type = employee_box.get()
                self.cursor.execute("SHOW COLUMNS FROM " + self.employee_view[employee_type])
                view_columns = self.cursor.fetchall()

                self.employee_tree = ttk.Treeview(self.root, columns=[c[0] for c in view_columns], show="headings")

                for c in view_columns:
                    self.employee_tree.heading(c[0], text=c[0])
                self.employee_tree.grid(row=2, column=0, columnspan=len(view_columns))

                self.cursor.execute("SELECT * FROM " + self.employee_view[employee_type])
                data_employees = self.cursor.fetchall()
                for row in data_employees:
                    self.employee_tree.insert("", "end", values=row)

            self.clear_window()
            (tk.Button(self.root, text="В главное меню", command=self.main_menu)
             .grid(row=0, column=3))

            employee_box = ttk.Combobox(self.root, values=list(self.employee_view.keys()))
            employee_box.bind("<<ComboboxSelected>>", refresh_employee_tree)
            employee_box.grid(row=1, column=0)

        super().main_menu()

        (tk.Label(self.root, text="Функции и процедуры")
         .grid(row=1, column=0))

        (tk.Button(self.root, text="Получить информацию о выступлении и купить билет",
                   command=get_performance_info)
         .grid(row=2, column=0))
        (tk.Button(self.root, text="Актеры, музыканты и продюссеры театра",
                   command=get_employees_info)
         .grid(row=3, column=0))