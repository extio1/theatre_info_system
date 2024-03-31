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
CREATE TABLE Seating_arrangements(
    id INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
    name VARCHAR(255)
)
//
CREATE TABLE Seating_places(
    id INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
    arrangement_id INT NOT NULL,
    name VARCHAR(255),
    price NUMERIC NOT NULL,

    CHECK(price >= 0),
    FOREIGN KEY(arrangement_id) REFERENCES Seating_arrangements(id)
        ON UPDATE CASCADE
        ON DELETE CASCADE
)
//
CREATE TABLE Repertoire(
    id INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
    performance_id INT NOT NULL,
    performance_date Date NOT NULL,
    ticket_sold INT NOT NULL DEFAULT 0,
    season_ticket_sold INT NOT NULL DEFAULT 0,
    seating_scheme INT,

    CHECK(ticket_sold >= 0),
    CHECK(season_ticket_sold >= 0),
    FOREIGN KEY(performance_id) REFERENCES Performances(id)
        ON UPDATE CASCADE
        ON DELETE CASCADE,
    FOREIGN KEY(seating_scheme) REFERENCES Seating_arrangements(id)
        ON UPDATE CASCADE
        ON DELETE SET NULL
)
//
CREATE TABLE Repertoire_history(
    id INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
    performance_id INT NOT NULL,
    performance_date Date NOT NULL,
    ticket_sold INT NOT NULL,
    season_ticket_sold INT NOT NULL,
    seating_scheme INT NOT NULL,

    CHECK(ticket_sold >= 0),
    CHECK(season_ticket_sold >= 0),
    FOREIGN KEY(seating_scheme) REFERENCES Seating_arrangements(id)
        ON UPDATE NO ACTION
        ON DELETE NO ACTION,
    FOREIGN KEY(performance_id) REFERENCES Performances(id)
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
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
    INSERT INTO Repertoire_history(id, performance_id, performance_date)
    VALUES(OLD.id, OLD.performance_id, OLD.performance_date);
//
