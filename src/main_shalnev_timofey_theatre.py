import tkinter as tk
from mysql.connector import connect, Error
from tkinter import messagebox
from tkinter import ttk

migrate_string = """CREATE TABLE Countries (
	id INT PRIMARY KEY AUTO_INCREMENT,
	name VARCHAR(255)
)
//
CREATE TABLE Education_Institution (
	id INT PRIMARY KEY AUTO_INCREMENT,
	name VARCHAR(512) NOT NULL
)
//
CREATE TABLE Employees (
	id INT PRIMARY KEY AUTO_INCREMENT,
	name VARCHAR(255) NOT NULL,
	surname VARCHAR(255) NOT NULL,
	patronymic VARCHAR(255),
	salary DECIMAL(10,3) NOT NULL,
	hire_date Date NOT NULL,
	birthday Date NOT NULL,
    CONSTRAINT salary_more_zero CHECK (salary >= 0),
    CONSTRAINT hire_more_birth CHECK (hire_date >= birthday)
)
//
CREATE TABLE Employee_education (
    employee_id INT NOT NULL,
    education_institution_id INT NOT NULL,

	FOREIGN KEY(employee_id) REFERENCES Employees(id)
	    ON UPDATE CASCADE
        ON DELETE CASCADE,

    FOREIGN KEY(education_institution_id) REFERENCES Education_Institution(id)
	    ON UPDATE CASCADE
        ON DELETE NO ACTION,

    PRIMARY KEY(employee_id, education_institution_id)
)
//
CREATE TABLE Awards (
    id INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
    employee_id INT NOT NULL,
    award_name VARCHAR(512) NOT NULL,
    competition_name VARCHAR(512) NOT NULL,

    FOREIGN KEY(employee_id) REFERENCES Employees(id)
        ON UPDATE CASCADE
        ON DELETE CASCADE
)
//
CREATE TABLE Titles (
    id INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
    employee_id INT NOT NULL,
    title_name VARCHAR(512) NOT NULL,

    FOREIGN KEY(employee_id) REFERENCES Employees(id)
        ON UPDATE CASCADE
        ON DELETE CASCADE
)
//
CREATE TABLE Tours (
    id INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
    employee_id INT NOT NULL,
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    outcome_tour BOOLEAN NOT NULL,
    FOREIGN KEY(employee_id) REFERENCES Employees(id)
        ON UPDATE CASCADE
        ON DELETE CASCADE
)
//
CREATE TABLE Actors (
    id INT PRIMARY KEY,
	height INT NOT NULL,
	weight INT NOT NULL,
	voice ENUM('бас', 'баритон', 'тенор', 'альт', 'меццо-сопрано', 'сопрано') NOT NULL,
	sex ENUM('мужской', 'женский') NOT NULL,
	country_id INT,

	CHECK(height >= 0),
	CHECK(weight >= 0),

	FOREIGN KEY(country_id) REFERENCES Countries(id)
	    ON UPDATE RESTRICT
        ON DELETE SET NULL,
    FOREIGN KEY(id) REFERENCES Employees(id)
        ON UPDATE CASCADE
        ON DELETE CASCADE
)
//
CREATE TABLE Producers (
    id INT PRIMARY KEY NOT NULL,
	FOREIGN KEY(id) REFERENCES Employees(id)
        ON UPDATE CASCADE
        ON DELETE CASCADE
)
//
CREATE TABLE Musicians (
    id INT PRIMARY KEY NOT NULL,
    FOREIGN KEY(id) REFERENCES Employees(id)
        ON UPDATE CASCADE
        ON DELETE CASCADE
)
//
CREATE TABLE Instruments (
    id INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
    name VARCHAR(512) NOT NULL
)
//
CREATE TABLE Musicians_Instruments (
    musician_id INT NOT NULL,
    instrument_id INT NOT NULL,

    FOREIGN KEY(musician_id) REFERENCES Musicians(id)
        ON UPDATE CASCADE
        ON DELETE CASCADE,
    FOREIGN KEY(instrument_id) REFERENCES Instruments(id)
        ON UPDATE CASCADE
        ON DELETE CASCADE,

    PRIMARY KEY(musician_id, instrument_id)
)
//
CREATE TABLE Authors(
    id INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
    country_id INT,
    name VARCHAR(255) NOT NULL,
	surname VARCHAR(255) NOT NULL,
	patronymic VARCHAR(255),
    birthday Date,
    death_date Date,

    FOREIGN KEY(country_id) REFERENCES Countries(id)
	    ON UPDATE RESTRICT
        ON DELETE SET NULL
)
//
CREATE TABLE Genres(
    id INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
    name VARCHAR(255) NOT NULL
)
//
CREATE TABLE Performances(
    id INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
    name VARCHAR(255) NOT NULL,
    conductor_id INT,
    producer_id INT,
    stage_id INT,
    premier_date Date NOT NULL,
    creation_date Date NOT NULL,
    author_id INT,
    genre_id INT,
    target_audience ENUM('0+', '12+', '16+', '18+') NOT NULL,

    FOREIGN KEY(conductor_id) REFERENCES Producers(id)
        ON UPDATE CASCADE
        ON DELETE SET NULL,

    FOREIGN KEY(producer_id) REFERENCES Producers(id)
        ON UPDATE CASCADE
        ON DELETE SET NULL,

    FOREIGN KEY(stage_id) REFERENCES Producers(id)
        ON UPDATE CASCADE
        ON DELETE SET NULL,

    FOREIGN KEY(author_id) REFERENCES Authors(id)
        ON UPDATE CASCADE
        ON DELETE SET NULL,

    FOREIGN KEY(genre_id) REFERENCES Genres(id)
        ON UPDATE CASCADE
        ON DELETE SET NULL,

    CONSTRAINT premier_more_create CHECK (premier_date >= creation_date)
)
//
CREATE TABLE Repertoire(
    id INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
    performance_id INT NOT NULL,
    performance_date Date NOT NULL,
    ticket_sold INT NOT NULL DEFAULT 0,
    season_ticket_sold INT NOT NULL DEFAULT 0,

    CHECK(ticket_sold >= 0),
    CHECK(season_ticket_sold >= 0),
    FOREIGN KEY(performance_id) REFERENCES Performances(id)
        ON UPDATE CASCADE
        ON DELETE CASCADE
)
//
CREATE TABLE Repertoire_history(
    id INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
    performance_id INT NOT NULL,
    performance_date Date NOT NULL,
    ticket_sold INT NOT NULL,
    season_ticket_sold INT NOT NULL,

    CHECK(ticket_sold >= 0),
    CHECK(season_ticket_sold >= 0),
    FOREIGN KEY(performance_id) REFERENCES Performances(id)
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
)
//
CREATE TABLE Prices(
    show_id INT NOT NULL,
    name VARCHAR(255) NOT NULL,
    price NUMERIC NOT NULL,
    amount INT NOT NULL DEFAULT 0,
    bought INT NOT NULL DEFAULT 0,

    CHECK(price >= 0),
    CHECK(bought <= amount),
    FOREIGN KEY(show_id) REFERENCES Repertoire(id)
        ON UPDATE CASCADE
        ON DELETE CASCADE,
    PRIMARY KEY(show_id, name)
)
//
CREATE TABLE Season_tickets(
    id INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    author_id INT,
    genre_id INT,

    FOREIGN KEY(author_id) REFERENCES Authors(id)
        ON UPDATE CASCADE
        ON DELETE SET NULL,
    FOREIGN KEY(genre_id) REFERENCES Genres(id)
        ON UPDATE CASCADE
        ON DELETE SET NULL
)
//
CREATE TRIGGER season_ticket_check_correctness_before_insert
BEFORE INSERT
ON Season_tickets FOR EACH ROW
BEGIN
    IF (NEW.genre_id IS NULL AND NEW.author_id IS NULL) THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT='Season ticket must have author or genre specified';
    END IF;
END;
//
CREATE TRIGGER season_ticket_add_repertoire_after_insert
AFTER INSERT
ON Season_tickets FOR EACH ROW
BEGIN
    UPDATE Repertoire r JOIN Performances p ON r.performance_id = p.id
    SET r.season_ticket_sold = r.season_ticket_sold + 1
    WHERE (author_id = NEW.author_id AND author_id IS NOT NULL AND NEW.author_id IS NOT NULL) OR
          (genre_id  = NEW.genre_id  AND genre_id  IS NOT NULL AND NEW.genre_id  IS NOT NULL);
END;
//
CREATE TRIGGER move_repertoire_history_on_delete
BEFORE DELETE
ON Repertoire FOR EACH ROW
    INSERT INTO Repertoire_history(id, performance_id, performance_date, ticket_sold, season_ticket_sold)
    VALUES(OLD.id, OLD.performance_id, OLD.performance_date, OLD.ticket_sold, OLD.season_ticket_sold);
//
CREATE FUNCTION get_current_repertoire_income()
RETURNS NUMERIC
READS SQL DATA
BEGIN
    DECLARE income NUMERIC;
    SET income = 0;
    SELECT SUM(p.price*p.bought) into income
    FROM Repertoire r
    JOIN Prices p ON p.show_id = r.id;
    RETURN income;
END;
//
CREATE PROCEDURE show_available_tickets(IN show_id INT)
BEGIN
    SELECT p.name, r.performance_date, CONCAT(a.name, " ", a.surname, " ",  COALESCE(a.patronymic, "")) AS author, g.name
    FROM Repertoire r
    JOIN Performances p ON r.performance_id = p.id
    JOIN Authors a ON p.author_id = a.id
    JOIN Genres g on p.genre_id = g.id
    WHERE r.id = show_id;

    SELECT name, price, amount, (amount-bought) AS available FROM Prices WHERE Prices.show_id = show_id;
END;
//"""

fill_string = """
INSERT INTO Countries (id,name) VALUES
(NULL, "Российская империя"),
(NULL, "СССР"),
(NULL, "Российская Федерация"),
(NULL, "Украина"),
(NULL, "Республика Беларусь"),
(NULL, "Конго"),
(NULL, "США"),
(NULL, "Армения"),
(NULL, "Великобритания")
//
INSERT INTO Education_Institution VALUES
(NULL, "Новосибирский Национальный Исследовательский Государственный Университет"),
(NULL, "Саратовская государственная консерватория им. Л.В. Собинова"),
(NULL, "Челябинский государственный институт культуры"),
(NULL, "Калужский государственный университет им. К.Э. Циолковского"),
(NULL, "Российская государственная специализированная академия искусств"),
(NULL, "Уфимский государственный институт искусств имени Загира Исмагилова "),
(NULL, "Московский информационно-технологический университет"),
(NULL, "Московский гуманитарный университет"),
(NULL, "Алтайский государственный институт культуры"),
(NULL, "Восточно-Сибирский государственный институт культуры ")
//
INSERT INTO Employees(id,name,surname,patronymic,salary, hire_date, birthday) VALUES
(NULL, "Иван", "Иванович", "Иванов", 51000.50, '2001-03-24', '1980-01-08'),
(NULL, "Иван", "Иванович", "Сергеев", 57000.52, '2002-01-14', '1999-02-18'),
(NULL, "Иван", "Сергеевич", "Иванов", 30440.50, '2003-04-29', '1978-03-28'),
(NULL, "Иван", "Сергеевич", "Сергеев", 20600, '2008-01-13', '1998-04-30'),
(NULL, "Сергей", "Иванович", "Иванов", 102000.50, '2001-06-21', '1977-05-11'),
(NULL, "Сергей", "Иванович", "Сергеев", 16700, '2003-10-3', '1990-06-28'),
(NULL, "Сергей", "Сергеевич", "Иванов", 52553.73, '2002-02-7', '1997-09-18'),
(NULL, "Сергей", "Сергеевич", "Сергеев", 19011.18, '2001-11-24', '1996-10-8')
//
INSERT INTO Employee_education(employee_id, education_institution_id) VALUES
(1, 1),
(2, 2),
(3, 1),
(4, 3),
(5, 1),
(6, 3),
(7, 5)
//
INSERT INTO Actors(id, height, weight, voice, sex, country_id) VALUES
(1, 180, 80, 'баритон', 'мужской', 3),
(3, 173, 64, 'бас', 'мужской', 4),
(5, 188, 70, 'тенор', 'мужской', 6),
(6, 191, 121, 'баритон', 'мужской', 3),
(7, 153, 61, 'бас', 'мужской', 3)
//
INSERT INTO Musicians VALUES
(2),
(4),
(6)
//
INSERT INTO Producers(id) VALUES
(1),
(3),
(7)
//
INSERT INTO Awards(id, employee_id, competition_name, award_name) VALUES
(NULL, 1, 'VI Всероссийский фестиваль-школа любительских театров В ГЛАВНОЙ РОЛИ', 'Лучший драматургический материал'),
(NULL, 3, 'I Международный многожанровый конкурс-фестиваль ЛЕГЕНДА', 'Лучшая мужская роль второго плана'),
(NULL, 3, 'V Всероссийский многожанровый конкурс-фестиваль современного искусства PRO-СТРАНСТВО', 'Лучший дебют'),
(NULL, 5, 'I Международный многожанровый конкурс-фестиваль ЛЕГЕНДА', 'Лучшая мужская роль первого плана'),
(NULL, 6, 'I Международный многожанровый конкурс-фестиваль ЛЕГЕНДА', 'Приз зрительских симпатий')
//
INSERT INTO Titles (id, employee_id, title_name) VALUES
(NULL, 5, 'Заслуженный деятель искусств Российской Федерации'),
(NULL, 1, 'Заслуженный деятель искусств РСФСР'),
(NULL, 6, 'Заслуженный деятель искусств Латвийской ССР')
//
INSERT INTO Tours(id, employee_id, start_date, end_date, outcome_tour) VALUES
(NULL, 6, '2024-01-24', '2024-04-24', 1),
(NULL, 1, '2024-03-01', '2024-05-20', 1)
//
INSERT INTO Instruments (id, name) VALUES
(NULL, "флейта"),
(NULL, "фортепиано"),
(NULL, "скрипка"),
(NULL, "бас"),
(NULL, "клавесин"),
(NULL, "терменвокс"),
(NULL, "треугольник"),
(NULL, "контрабас")
//
INSERT INTO Musicians_Instruments (musician_id, instrument_id) VALUES
(2, 1),
(4, 2),
(6, 3),
(6, 5),
(6, 6)
//
INSERT INTO Authors(id, country_id, name, surname, patronymic, birthday, death_date) VALUES
(NULL, 3, 'Александр', 'Николаевич', 'Островский', '1823-03-31', '1886-02-06'),
(NULL, 3, 'Максим', 'Горький', NULL, '1868-03-16', '1936-02-18'),
(NULL, 9, 'Уильям', 'Шекспир', NULL, '1564-04-01', '1616-04-23')
//
INSERT INTO Genres(id, name) VALUES
(NULL, 'буффонада'),
(NULL, 'мюзикл'),
(NULL, 'драма'),
(NULL, 'комедия'),
(NULL, 'мелодрама'),
(NULL, 'мистерия'),
(NULL, 'монодрама'),
(NULL, 'пастораль'),
(NULL, 'соти'),
(NULL, 'трагедия'),
(NULL, 'трагикомедия')
//
INSERT INTO Performances VALUES
(NULL, 'Свои люди - сочтёмся', 1, 3, 7, '2018-04-20', '1849-01-01', 1, 3, '16+'),
(NULL, 'Гроза', 3, 3, 1, '2016-09-19', '1859-01-01', 1, 3, '12+'),
(NULL, 'Правда — хорошо, а счастье лучше', 1, 7, 7, '2021-02-10', '1879-01-01', 1, 4, '12+'),
(NULL, 'На дне', 1, 1, 7, '2022-03-11', '1901-01-01', 2, 3, '16+'),
(NULL, 'Мещане', 3, 1, 7, '2021-07-22', '1901-01-01', 2, 3, '16+'),
(NULL, 'Ромео и Джульетта', 3, 1, 7, '2022-06-21', '1595-01-01', 3, 3, '16+'),
(NULL, 'Отелло', 3, 1, 1, '2023-06-21', '1604-01-01', 3, 3, '16+'),
(NULL, 'Гамлет', 3, 3, 1, '2023-07-18', '1600-01-01', 3, 3, '16+')
//
INSERT INTO Repertoire(id, performance_id, performance_date) VALUES
(NULL, 1, '2024-01-30'),
(NULL, 2, '2024-02-10'),
(NULL, 4, '2024-02-25'),
(NULL, 5, '2024-03-17'),
(NULL, 6, '2024-04-11'),
(NULL, 7, '2024-05-10')
//
INSERT INTO Prices(show_id, name, price, amount) VALUES
(1, 'партер', 4500, 50),
(1, 'высокий партер', 4800, 40),
(1, 'амфитеатр', 3500, 60),
(1, 'ложа', 25000, 16),
(2, 'партер', 6500, 50),
(2, 'высокий партер', 6800, 40),
(2, 'амфитеатр', 5500, 60),
(2, 'ложа', 30001, 16),
(3, 'партер', 4500.50, 50),
(3, 'высокий партер', 6500, 40),
(3, 'амфитеатр', 3700, 60),
(3, 'ложа', 19000, 16),
(4, 'партер', 5500, 50),
(4, 'высокий партер', 4500, 40),
(4, 'амфитеатр', 5500, 60),
(4, 'ложа', 10000, 16),
(5, 'партер', 2500, 50),
(5, 'высокий партер', 3800, 40),
(5, 'амфитеатр', 4500, 60),
(5, 'ложа', 22000, 16),
(6, 'партер', 4800, 50),
(6, 'высокий партер', 5400, 40),
(6, 'амфитеатр', 4200, 60),
(6, 'ложа', 22000, 16)
//
INSERT INTO Season_tickets(id, start_date, end_date, author_id, genre_id) VALUES
(NULL, '2024-01-30', '2024-05-10', 1, NULL)
//
"""

config = {
    "host": "localhost",
    "database": "theatre"
}

class UserInterface:
    pass

class VisitorInterface(UserInterface):

class DatabaseApp:
    def __init__(self):
        self.user_interface = None

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

        tk.Label(self.root, text="Роль:").pack()
        self.role_combobox = ttk.Combobox(self.root, values=["Посетитель", "Директор"])
        self.role_combobox.pack()

        tk.Button(self.root, text="Вход", command=self.auth_to_database).pack()

        self.root.mainloop()

    def auth_to_database(self):
        host = self.host_entry.get()
        login = self.login_entry.get()
        password = self.password_entry.get()

        try:
            self.connection = connect(host=host, user=login, password=password)
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
        def migrate():
            from mysql.connector import Error
            try:
                with self.connection.cursor() as cursor:
                    cursor.execute("DROP DATABASE IF EXISTS " + config["database"])
                    cursor.execute("CREATE DATABASE " + config["database"])
                    cursor.execute("USE " + config["database"])

                    for create_table_query in migrate_string.split("//"):
                        print(create_table_query)
                        if len(create_table_query) > len("CREATE"):
                            cursor.execute(create_table_query)
                            self.connection.commit()

                messagebox.showinfo(title="Success", message="Success")
            except Error as e:
                messagebox.showerror(e.msg)

        def fill():
            from mysql.connector import Error
            try:
                with self.connection.cursor() as cursor:
                    for insert_table_query in fill_string.split("//"):
                        if len(insert_table_query) > len("INSERT"):
                            print(insert_table_query)
                            cursor.execute(insert_table_query)
                    self.connection.commit()

                    messagebox.showinfo(title="Success", message="Success")
            except Error as e:
                messagebox.showerror(e.msg)

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
                    self.cursor.execute("call show_available_tickets(" + id_entry.get() + ")")
                    show = self.cursor.fetchall()
                    show = show[0]
                    self.cursor.nextset()
                    prices = self.cursor.fetchall()

                    pp = tk.Toplevel(self.root)
                    pp.title("Информация о выступлении")
                    pp.geometry("800x300")
                    tk.Label(pp, text="Спектакль: \"" + show[0] + "\"").grid(row=0, column=0)
                    tk.Label(pp, text="Дата: \"" + show[1].strftime("%d/%m/%Y") + "\"").grid(row=1, column=0)
                    tk.Label(pp, text="Автор: \"" + show[2] + "\"").grid(row=2, column=0)
                    tk.Label(pp, text="Жанр: \"" + show[3] + "\"").grid(row=3, column=0)
                    tk.Label(pp, text="Место:").grid(row=4, column=0)
                    tk.Label(pp, text="Цена:").grid(row=4, column=1)
                    tk.Label(pp, text="Всего билетов:").grid(row=4, column=2)
                    tk.Label(pp, text="Свободно билетов:").grid(row=4, column=3)

                    for m in range(len(prices)):
                        for k in range(0, len(prices[m])):
                            tk.Label(pp, text=prices[m][k]).grid(row=5 + m, column=k)

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
         .grid(row=N_ROWS + 1, column=0))
        (tk.Button(self.root, text="Доход за текущий сезон", command=get_repertoire_income)
         .grid(row=N_ROWS + 2, column=0))
        (tk.Button(self.root, text="Получить информацию о выступлении", command=get_performance_info)
         .grid(row=N_ROWS + 2, column=1))

        (tk.Label(self.root, text="Управление базой данных")
         .grid(row=N_ROWS + 3, column=0))
        (tk.Button(self.root, text="Выполнить миграцию", command=migrate)
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

            (tk.Button(self.root, text="В главное меню", command=self.show_main_menu)
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


def main():
    DatabaseApp()


if __name__ == "__main__":
    main()
