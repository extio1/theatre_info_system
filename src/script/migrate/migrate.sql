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
//