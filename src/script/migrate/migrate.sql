CREATE TABLE Countries (
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
CREATE TABLE Employee_login (
    employee_id INT PRIMARY KEY,
    login VARCHAR(255) NOT NULL UNIQUE,

    FOREIGN KEY(employee_id) REFERENCES Employees(id)
	    ON UPDATE CASCADE
        ON DELETE CASCADE
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
	height INT,
	weight INT,
	voice ENUM('бас', 'баритон', 'тенор', 'альт', 'меццо-сопрано', 'сопрано'),
	sex ENUM('мужской', 'женский'),
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
CREATE TABLE Roles(
    id INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
    actor_id INT,
    show_id INT,
    name VARCHAR(512) NOT NULL,
    type ENUM('дублер', 'основная'),

    FOREIGN KEY(actor_id) REFERENCES Actors(id)
        ON UPDATE CASCADE
        ON DELETE SET NULL,
    FOREIGN KEY(show_id) REFERENCES Repertoire(id)
        ON UPDATE CASCADE
        ON DELETE SET NULL
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
    SELECT name, price, amount, (amount-bought) AS available FROM Prices WHERE Prices.show_id = show_id;
END;
//
CREATE VIEW Roles_view AS
SELECT r.actor_id,
       p.name AS performance_name,
       rp.performance_date,
       r.name AS role_name,
       r.type
FROM Roles r
INNER JOIN Repertoire rp ON r.show_id=rp.id
INNER JOIN Performances p ON p.id = rp.performance_id;
//
CREATE VIEW Repertoire_info_view AS
SELECT r.id, p.name, r.performance_date, CONCAT(a.name, " ", a.surname, " ",  COALESCE(a.patronymic, "")) AS author,
       g.name AS genre
    FROM Repertoire r
    JOIN Performances p ON r.performance_id = p.id
    JOIN Authors a ON p.author_id = a.id
    JOIN Genres g on p.genre_id = g.id;
//
CREATE PROCEDURE buy_ticket(IN buy_show INT, IN buy_place VARCHAR(255), IN buy_amount INT)
BEGIN
    DECLARE available_tickets INT;

    SELECT amount - bought INTO available_tickets
    FROM Prices
    WHERE show_id = buy_show AND name = buy_place;

    IF available_tickets >= buy_amount THEN
        UPDATE Prices
        SET bought = bought + buy_amount
        WHERE show_id = buy_show AND name = buy_place;
    ELSE
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT='Указанное число билетов для покупки больше числа доступных для покупки';
    END IF;
END;
//
CREATE VIEW Actors_private_view
AS
    SELECT e.id, CONCAT(e.name, " ", e.surname, " ",  COALESCE(e.patronymic, "")) AS name,
           a.height, a.weight, c.name AS country_name, a.voice,
           e.salary, e.hire_date, e.birthday, ti.title_name, aw.award_name,
           aw.competition_name
    FROM Actors a
    LEFT JOIN Employees e ON a.id = e.id
    LEFT JOIN Countries c ON a.country_id = c.id
    LEFT JOIN Awards aw ON e.id = aw.employee_id
    LEFT JOIN Titles ti ON e.id = ti.employee_id;
//
CREATE VIEW Actors_public_view
AS
    SELECT e.id, CONCAT(e.name, " ", e.surname, " ",  COALESCE(e.patronymic, "")) AS name,
           a.height, a.weight, c.name AS country_name, a.voice,
           ti.title_name, aw.award_name,
           aw.competition_name
    FROM Actors a
    LEFT JOIN Employees e ON a.id = e.id
    LEFT JOIN Countries c ON a.country_id = c.id
    LEFT JOIN Awards aw ON e.id = aw.employee_id
    LEFT JOIN Titles ti ON e.id = ti.employee_id;
//
CREATE VIEW Musicians_private_view
AS
    SELECT e.id, CONCAT(e.name, " ", e.surname, " ",  COALESCE(e.patronymic, "")) AS name,
           i.name AS musical_instruments,
           ti.title_name,
           e.salary, e.hire_date, e.birthday, aw.award_name, aw.competition_name
    FROM Musicians m
    JOIN Employees e ON m.id = e.id
    LEFT JOIN Awards aw ON e.id = aw.employee_id
    LEFT JOIN Titles ti ON e.id = ti.employee_id
    LEFT JOIN Musicians_Instruments mi ON e.id = mi.musician_id
    LEFT JOIN Instruments i ON mi.instrument_id = i.id;
//
CREATE VIEW Musicians_public_view
AS
    SELECT e.id, CONCAT(e.name, " ", e.surname, " ",  COALESCE(e.patronymic, "")) AS name,
           i.name AS musical_instruments,
           ti.title_name, aw.award_name, aw.competition_name
    FROM Musicians m
    JOIN Employees e ON m.id = e.id
    LEFT JOIN Awards aw ON e.id = aw.employee_id
    LEFT JOIN Titles ti ON e.id = ti.employee_id
    LEFT JOIN Musicians_Instruments mi ON e.id = mi.musician_id
    LEFT JOIN Instruments i ON mi.instrument_id = i.id;
//
CREATE VIEW Producers_private_view
AS
    SELECT e.id, CONCAT(e.name, " ", e.surname, " ",  COALESCE(e.patronymic, "")) AS name,
           ti.title_name, aw.award_name,
           e.salary, e.hire_date, e.birthday, aw.competition_name
    FROM Producers p
    JOIN Employees e ON p.id = e.id
    LEFT JOIN Awards aw ON e.id = aw.employee_id
    LEFT JOIN Titles ti ON e.id = ti.employee_id;
//
CREATE VIEW Producers_public_view
AS
    SELECT CONCAT(e.name, " ", e.surname, " ",  COALESCE(e.patronymic, "")) AS name,
           ti.title_name, aw.award_name, aw.competition_name, e.id
    FROM Producers p
    JOIN Employees e ON p.id = e.id
    LEFT JOIN Awards aw ON e.id = aw.employee_id
    LEFT JOIN Titles ti ON e.id = ti.employee_id;
//
CREATE VIEW Workers_private_view
AS
    SELECT e.id, CONCAT(e.name, " ", e.surname, " ",  COALESCE(e.patronymic, "")) AS name,
    e.salary, e.hire_date, e.birthday,
    CONCAT(IF(a.id IS NULL, '', 'актёр '),
           IF(m.id IS NULL, '', 'музыкант '),
           IF(p.id IS NULL, '', 'продюссер'),
           IF(p.id IS NULL AND m.id IS NULL AND a.id IS NULL, 'служащий', '')
           ) AS title
    FROM Employees e
    LEFT JOIN Actors a ON e.id = a.id
    LEFT JOIN Musicians m ON e.id = m.id
    LEFT JOIN Producers p ON e.id = p.id;
//
CREATE VIEW Workers_public_view
AS
    SELECT CONCAT(e.name, " ", e.surname, " ",  COALESCE(e.patronymic, "")) AS name,
    CONCAT(IF(a.id IS NULL, '', 'актёр '),
           IF(m.id IS NULL, '', 'музыкант '),
           IF(p.id IS NULL, '', 'продюссер'),
           IF(p.id IS NULL AND m.id IS NULL AND a.id IS NULL, 'служащий', '')
           ) AS title, e.id as id
    FROM Employees e
    LEFT JOIN Actors a ON e.id = a.id
    LEFT JOIN Musicians m ON e.id = m.id
    LEFT JOIN Producers p ON e.id = p.id;
//
CREATE PROCEDURE CreateEmployee(
    IN name VARCHAR(256),
    IN surname VARCHAR(256),
    IN patronymic VARCHAR(256),
    IN salary NUMERIC,
    IN hire_date DATE,
    IN birthday DATE,
    OUT id INT
    )
BEGIN
    INSERT INTO Employees(id, surname, name, patronymic, salary, hire_date, birthday)
    VALUES
    (
    NULL,
    name,
    surname,
    patronymic,
    salary,
    hire_date,
    birthday
    );
    SELECT LAST_INSERT_ID() INTO id;
END;
//
CREATE PROCEDURE InsertIntoProducers_private_view(
    IN name VARCHAR(256),
    IN surname VARCHAR(256),
    IN patronymic VARCHAR(256),
    IN salary NUMERIC,
    IN hire_date DATE,
    IN birthday DATE
    )
BEGIN
    DECLARE x INT;
    CALL CreateEmployee(name, surname, patronymic, salary, hire_date, birthday, x);
    INSERT INTO Producers() VALUES (x);
END;
//
CREATE PROCEDURE InsertIntoMusicians_private_view(
    IN name VARCHAR(256),
    IN surname VARCHAR(256),
    IN patronymic VARCHAR(256),
    IN salary NUMERIC,
    IN hire_date DATE,
    IN birthday DATE
    )
BEGIN
    DECLARE x INT;
    CALL CreateEmployee(name, surname, patronymic, salary, hire_date, birthday, x);
    INSERT INTO Musicians() VALUES (x);
END;
//
CREATE PROCEDURE InsertIntoActors_private_view(
    IN name VARCHAR(256),
    IN surname VARCHAR(256),
    IN patronymic VARCHAR(256),
    IN salary NUMERIC,
    IN hire_date DATE,
    IN birthday DATE
    )
BEGIN
    DECLARE id INT;

    CALL CreateEmployee(name, surname, patronymic, salary, hire_date, birthday, id);

    INSERT INTO Actors(id) VALUE (id);
END;
//
CREATE PROCEDURE InsertIntoWorkers_private_view(
    IN name VARCHAR(256),
    IN surname VARCHAR(256),
    IN patronymic VARCHAR(256),
    IN salary NUMERIC,
    IN hire_date DATE,
    IN birthday DATE
    )
BEGIN
    DECLARE x INT;
    CALL CreateEmployee(name, surname, patronymic, salary, hire_date, birthday, x);
END;
//
CREATE FUNCTION get_my_employee_id(user_login VARCHAR(256))
RETURNS INT
READS SQL DATA
BEGIN
    DECLARE id INT;
    SELECT e.employee_id INTO id FROM Employee_login e WHERE e.login=user_login;
    RETURN id;
END
//
CREATE ROLE IF NOT EXISTS 'director'
//
CREATE ROLE IF NOT EXISTS 'client'
//
CREATE ROLE IF NOT EXISTS 'producer'
//
CREATE ROLE IF NOT EXISTS 'actor'
//
CREATE ROLE IF NOT EXISTS 'musician'
//
CREATE ROLE IF NOT EXISTS 'worker'
//
FLUSH PRIVILEGES;
//
GRANT SHOW DATABASES ON *.* TO 'director'
//
GRANT USAGE ON theatre.* TO 'director'
//
GRANT EXECUTE ON FUNCTION theatre.get_current_repertoire_income TO 'director'
//
GRANT SELECT, DELETE ON theatre.Employees TO 'director'
//
GRANT SELECT ON theatre.Musicians_private_view TO 'director'
//
GRANT SELECT ON theatre.Workers_private_view TO 'director'
//
GRANT SELECT ON theatre.Actors_private_view TO 'director'
//
GRANT SELECT ON theatre.Producers_private_view TO 'director'
//
GRANT SELECT, DELETE, INSERT ON theatre.Employee_login TO 'director'
//
GRANT SUPER ON *.* TO 'director'
//
GRANT EXECUTE ON PROCEDURE theatre.InsertIntoMusicians_private_view TO 'director'
//
GRANT EXECUTE ON PROCEDURE theatre.InsertIntoActors_private_view TO 'director'
//
GRANT EXECUTE ON PROCEDURE theatre.InsertIntoProducers_private_view TO 'director'
//
GRANT EXECUTE ON PROCEDURE theatre.InsertIntoWorkers_private_view TO 'director'
//
GRANT DELETE ON TABLE theatre.Employees TO 'director'
//
GRANT CREATE USER ON *.* TO 'director';
//
FLUSH PRIVILEGES;
//
GRANT SHOW DATABASES ON *.* TO 'client'
//
GRANT USAGE ON theatre.* TO 'client'
//
GRANT SELECT ON theatre.Repertoire_info_view TO 'client'
//
GRANT SELECT ON theatre.Musicians_public_view TO 'client'
//
GRANT SELECT ON theatre.Workers_public_view TO 'client'
//
GRANT SELECT ON theatre.Actors_public_view TO 'client'
//
GRANT SELECT ON theatre.Producers_public_view TO 'client'
//
GRANT EXECUTE ON PROCEDURE theatre.show_available_tickets TO 'client'
//
GRANT EXECUTE ON PROCEDURE theatre.buy_ticket TO 'client'
//
FLUSH PRIVILEGES
//
GRANT USAGE ON theatre.* TO 'actor'
//
GRANT SELECT ON theatre.Roles TO 'actor'
//
GRANT EXECUTE ON FUNCTION theatre.get_my_employee_id TO 'actor'
//
GRANT SELECT ON theatre.Roles_view TO 'actor'
//
GRANT SELECT ON theatre.Workers_public_view TO 'actor'
//
FLUSH PRIVILEGES
//