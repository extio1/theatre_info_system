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
(NULL, 1, 'VI Всероссийский фестиваль-школа любительских театров \'В ГЛАВНОЙ РОЛИ\'', 'Лучший драматургический материал'),
(NULL, 3, 'I Международный многожанровый конкурс-фестиваль "ЛЕГЕНДА"', 'Лучшая мужская роль второго плана'),
(NULL, 3, 'V Всероссийский многожанровый конкурс-фестиваль современного искусства \'PRO-СТРАНСТВО\'', 'Лучший дебют'),
(NULL, 5, 'I Международный многожанровый конкурс-фестиваль "ЛЕГЕНДА"', 'Лучшая мужская роль первого плана'),
(NULL, 6, 'I Международный многожанровый конкурс-фестиваль "ЛЕГЕНДА"', 'Приз зрительских симпатий')
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
INSERT INTO Seating_arrangements(id, name) VALUES
(1, 'Большой зал "НОВАТ"')
//
INSERT INTO Seating_places(id, arrangement_id, name, price) VALUES
(NULL, 1, 'партер', 4500),
(NULL, 1, 'высокий партер', 4800),
(NULL, 1, 'амфитеарт', 3500),
(NULL, 1, 'ложа', 20000)
//
INSERT INTO Repertoire(id, performance_id, performance_date, seating_scheme) VALUES
(NULL, 1, '2024-01-30', 1),
(NULL, 2, '2024-02-10', 1),
(NULL, 4, '2024-02-25', 1),
(NULL, 5, '2024-03-17', 1),
(NULL, 6, '2024-04-11', 1),
(NULL, 7, '2024-05-10', 1)
//
INSERT INTO Season_tickets(id, start_date, end_date, author_id, genre_id) VALUES
(NULL, '2024-01-30', '2024-05-10', 1, NULL)
//