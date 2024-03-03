CREATE TABLE Education_Institution (
	id INT PRIMARY KEY AUTO_INCREMENT,
	name VARCHAR(512) NOT NULL
);

CREATE TABLE Employees (
	id INT PRIMARY KEY AUTO_INCREMENT,
	name VARCHAR(255) NOT NULL,
	surname VARCHAR(255) NOT NULL,
	patronymic VARCHAR(255) NOT NULL,
	salary DECIMAL(10,3) NOT NULL,
	hire_date Date NOT NULL,
	birthday Date NOT NULL,
    CONSTRAINT salary_more_zero CHECK (salary >= 0),
    CONSTRAINT hire_more_birth CHECK (hire_date >= birthday)
);

CREATE TABLE Employee_education (
    employee_id INT NOT NULL,
    education_institution_id INT NOT NULL,

	FOREIGN KEY(employee_id)
	    REFERENCES Employees(id)
	    ON UPDATE CASCADE
        ON DELETE CASCADE,

    FOREIGN KEY(education_institution_id)
	    REFERENCES Education_Institution(id)
	    ON UPDATE CASCADE
        ON DELETE CASCADE,

    PRIMARY KEY(employee_id, education_institution_id)
);

CREATE TABLE Countries (
	id INT PRIMARY KEY AUTO_INCREMENT,
	name VARCHAR(255)
);

CREATE TABLE Actors (
    id INT PRIMARY KEY AUTO_INCREMENT,
	height INT NOT NULL,
	weight INT NOT NULL,
	voice ENUM('бас', 'баритон', 'тенор', 'альт', 'меццо-сопрано', 'сопрано') NOT NULL,
	country_id INT,

	CHECK(height >= 0),
	CHECK(weight >= 0),

	FOREIGN KEY(country_id)
	    REFERENCES Countries(id)
	    ON UPDATE RESTRICT
        ON DELETE SET NULL,
    FOREIGN KEY(id)
        REFERENCES Employees(id)
        ON UPDATE CASCADE
        ON DELETE CASCADE
);

CREATE TABLE Workers (
    id INT PRIMARY KEY NOT NULL,
	FOREIGN KEY(id)
	    REFERENCES Employees(id)
	    ON UPDATE CASCADE
	    ON DELETE CASCADE
);

CREATE TABLE Producers (
    id INT PRIMARY KEY NOT NULL,
	FOREIGN KEY(id)
        REFERENCES Employees(id)
        ON UPDATE CASCADE
        ON DELETE CASCADE
);

CREATE TABLE Musicians (
    id INT PRIMARY KEY NOT NULL,
    FOREIGN KEY(id)
        REFERENCES Employees(id)
        ON UPDATE CASCADE
        ON DELETE CASCADE
);

CREATE TABLE Directors (
    id INT PRIMARY KEY NOT NULL,
	FOREIGN KEY(id)
	    REFERENCES Employees(id)
	    ON UPDATE CASCADE
	    ON DELETE CASCADE
);

CREATE TABLE Titles (
	id INT PRIMARY KEY AUTO_INCREMENT,
    employee_id INT NOT NULL,
	title_name VARCHAR(512) NOT NULL,

	FOREIGN KEY(employee_id)
        REFERENCES Employees(id)
        ON UPDATE CASCADE
        ON DELETE CASCADE
);