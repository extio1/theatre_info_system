CREATE TABLE Countries (
	id INT PRIMARY KEY AUTO_INCREMENT,
	name VARCHAR(255)
);

CREATE TABLE Education_Institution (
	id INT PRIMARY KEY AUTO_INCREMENT,
	name VARCHAR(512) NOT NULL
);

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
);

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
);

CREATE TABLE Awards (
    id INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
    employee_id INT NOT NULL,
    award_name VARCHAR(512) NOT NULL,
    competition_name VARCHAR(512) NOT NULL,

    FOREIGN KEY(employee_id) REFERENCES Employees(id)
        ON UPDATE CASCADE
        ON DELETE CASCADE
);

CREATE TABLE Titles (
    id INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
    employee_id INT NOT NULL,
    title_name VARCHAR(512) NOT NULL,

    FOREIGN KEY(employee_id) REFERENCES Employees(id)
        ON UPDATE CASCADE
        ON DELETE CASCADE
);

CREATE TABLE Tours (
    id INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
    employee_id INT NOT NULL,
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    outcome_tour BOOLEAN NOT NULL,
    FOREIGN KEY(employee_id) REFERENCES Employees(id)
        ON UPDATE CASCADE
        ON DELETE CASCADE
);

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
);

CREATE TABLE Producers (
    id INT PRIMARY KEY NOT NULL,
	FOREIGN KEY(id) REFERENCES Employees(id)
        ON UPDATE CASCADE
        ON DELETE CASCADE
);

CREATE TABLE Musicians (
    id INT PRIMARY KEY NOT NULL,
    FOREIGN KEY(id) REFERENCES Employees(id)
        ON UPDATE CASCADE
        ON DELETE CASCADE
);

CREATE TABLE Instruments (
    id INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
    name VARCHAR(512) NOT NULL
);

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
);

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
);

CREATE TABLE Genres(
    id INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
    name VARCHAR(255) NOT NULL
);

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
);

CREATE TABLE Repertoire(
    id INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
    performance_id INT NOT NULL,
    performance_date Date NOT NULL,

    FOREIGN KEY(performance_id) REFERENCES Performances(id)
        ON UPDATE CASCADE
        ON DELETE CASCADE
);

CREATE TABLE Repertoire_history(
    id INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
    performance_id INT,
    performance_date Date NOT NULL,

    FOREIGN KEY(performance_id) REFERENCES Performances(id)
        ON UPDATE CASCADE
        ON DELETE SET NULL
);

CREATE TRIGGER move_repertoire_history_on_delete
BEFORE DELETE
ON Repertoire
FOR EACH ROW
    INSERT INTO Repertoire_history(id, performance_id, performance_date)
    VALUES(OLD.id, OLD.performance_id, OLD.performance_date);
