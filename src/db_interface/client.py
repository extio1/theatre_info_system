from mysql.connector import Error, errors, errorcode
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk

from .interface import UserInterface
from .gui_screens.client_main_menu import client_main_menu
from .gui_screens.client_repertoire_menu import client_repertoire_menu


class VisitorInterface(UserInterface):
    def __init__(self, root, connection, db_app):
        super().__init__(root, connection, db_app)
        self.widgets = None
        self.employee_view = {'Продюссер': 'Producers_public_view',
                              'Актёр': 'Actors_public_view',
                              'Музыкант': 'Musicians_public_view',
                              }

        self.performances = []
        self.performance_names_list = []
        self.current_performance = None

    def main_menu(self):
        def repertoire():
            def refresh_info():
                self.cursor.execute('SELECT * FROM Repertoire_info_view ORDER BY performance_date')
                self.performances = self.cursor.fetchall()
                self.performance_names_list = [str(p[2]) + ':' + str(p[1]) for p in self.performances]
                self.current_performance = self.performances[0]

            '''
                performance:
                    0: id (int)
                    1: name (string)
                    2: date (date)
                    3: author (string)
                    4: genre (string)
            '''

            def refresh(a):
                if self.widgets['listbox_repertoire'].curselection():
                    selected_index = self.widgets['listbox_repertoire'].curselection()[0]
                    self.current_performance = self.performances[selected_index]

                self.widgets['name_info']['text'] = self.current_performance[1]
                self.widgets['date_info']['text'] = self.current_performance[2]
                self.widgets['author_info']['text'] = self.current_performance[3]
                self.widgets['genre_info']['text'] = self.current_performance[4]

                self.cursor.execute(
                    "call show_available_tickets(" + str(self.current_performance[0]) + ")"
                )

                prices = self.cursor.fetchall()
                for m in range(len(prices)):
                    for k in range(1, len(prices[m])):
                        widget_name = str(m + 1) + str(k) + "_info"
                        self.widgets[widget_name]['text'] = prices[m][k]

                try:
                    self.cursor.nextset()  # иначе command out of sync
                except Error:
                    pass

            def buy_ticket():
                try:
                    show_id = self.current_performance[0]
                    place_name = self.widgets['combo_box_place'].get()
                    amount = self.widgets['entry_n_tickets'].get()

                    self.cursor.callproc('buy_ticket', [show_id, place_name, amount])

                    messagebox.showinfo("Покупка",
                                        "Операция прошла успешно. " +
                                        "Было куплено " + str(amount) + " билетов в " +
                                        str(place_name),
                                        parent=self.root)
                    self.connection.commit()

                    refresh(None)
                except errors.DatabaseError as err:
                    messagebox.showerror("Ошибка",
                                         "Произошла ошибка:" + str(err),
                                         parent=self.root)

            refresh_info()
            self.root, self.widgets = (
                client_repertoire_menu(self.root,
                                       buy_f=buy_ticket,
                                       back_f=self.main_menu,
                                       repertoire_options=self.performance_names_list,
                                       repertoire_list_on_select=refresh)
            )

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

        self.root, self.widgets = (
            client_main_menu(self.root, repertoire, get_employees_info)
        )

        self.root.mainloop()
