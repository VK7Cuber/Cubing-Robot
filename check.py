import sqlite3
# -*- coding: utf-8 -*-

# Создаем или подключаемся к базе данных
connection = sqlite3.connect('patterns_data.sqlite')  # Название вашей базы данных
cursor = connection.cursor()

# Ваш SQL-код в виде строки
sql_script = """

PRAGMA foreign_keys = off;
BEGIN TRANSACTION;

DROP TABLE IF EXISTS patterns;

CREATE TABLE IF NOT EXISTS patterns (
    name      TEXT,
    link      TEXT,
    algorithm TEXT
);

INSERT INTO patterns (
                         name,
                         link,
                         algorithm
                     )
                     VALUES (
                         'Точки',
                         'images/patterns/uz0.png',
                         'algorithm'
                     );

INSERT INTO patterns (
                         name,
                         link,
                         algorithm
                     )
                     VALUES (
                         'Шахматы',
                         'images/patterns/uz1.png',
                         'algorithm'
                     );

INSERT INTO patterns (
                         name,
                         link,
                         algorithm
                     )
                     VALUES (
                         'Шахматы с точками',
                         'images/patterns/uz2.png',
                         'algorithm'
                     );

INSERT INTO patterns (
                         name,
                         link,
                         algorithm
                     )
                     VALUES (
                         'Зигзаг',
                         'images/patterns/uz3.png',
                         'algorithm'
                     );

INSERT INTO patterns (
                         name,
                         link,
                         algorithm
                     )
                     VALUES (
                         'Четыре Z',
                         'images/patterns/uz4.png',
                         'algorithm'
                     );

INSERT INTO patterns (
                         name,
                         link,
                         algorithm
                     )
                     VALUES (
                         'Крест Пламмера',
                         'images/patterns/uz6.png',
                         'algorithm'
                     );

INSERT INTO patterns (
                         name,
                         link,
                         algorithm
                     )
                     VALUES (
                         'Крест Кристмана',
                         'images/patterns/uz7.png',
                         'algorithm'
                     );

INSERT INTO patterns (
                         name,
                         link,
                         algorithm
                     )
                     VALUES (
                         'Шахматы 3-го порядка',
                         'images/patterns/uz8.png',
                         'algorithm'
                     );

INSERT INTO patterns (
                         name,
                         link,
                         algorithm
                     )
                     VALUES (
                         'Шахматы 6-го порядка',
                         'images/patterns/uz9.png',
                         'algorithm'
                     );

INSERT INTO patterns (
                         name,
                         link,
                         algorithm
                     )
                     VALUES (
                         '6 букв Н',
                         'images/patterns/uz10.png',
                         'algorithm'
                     );

INSERT INTO patterns (
                         name,
                         link,
                         algorithm
                     )
                     VALUES (
                         '6 минусов',
                         'images/patterns/uz11.png',
                         'algorithm'
                     );

INSERT INTO patterns (
                         name,
                         link,
                         algorithm
                     )
                     VALUES (
                         'Диагональные столбики',
                         'images/patterns/uz12.png',
                         'algorithm'
                     );

INSERT INTO patterns (
                         name,
                         link,
                         algorithm
                     )
                     VALUES (
                         'Столбики с крестом',
                         'images/patterns/uz14.png',
                         'algorithm'
                     );

INSERT INTO patterns (
                         name,
                         link,
                         algorithm
                     )
                     VALUES (
                         'Столбики с шахматным крестом',
                         'images/patterns/uz15.png',
                         'algorithm'
                     );

INSERT INTO patterns (
                         name,
                         link,
                         algorithm
                     )
                     VALUES (
                         'Столбики с крышей',
                         'images/patterns/uz16.png',
                         'algorithm'
                     );

INSERT INTO patterns (
                         name,
                         link,
                         algorithm
                     )
                     VALUES (
                         '4 буквы П',
                         'images/patterns/uz17.png',
                         'algorithm'
                     );

INSERT INTO patterns (
                         name,
                         link,
                         algorithm
                     )
                     VALUES (
                         '4 буквы Т',
                         'images/patterns/uz18.png',
                         'algorithm'
                     );

INSERT INTO patterns (
                         name,
                         link,
                         algorithm
                     )
                     VALUES (
                         'Буквы L',
                         'images/patterns/uz19.png',
                         'algorithm'
                     );

INSERT INTO patterns (
                         name,
                         link,
                         algorithm
                     )
                     VALUES (
                         'Пасьянс 1',
                         'images/patterns/uz22.png',
                         'algorithm'
                     );

INSERT INTO patterns (
                         name,
                         link,
                         algorithm
                     )
                     VALUES (
                         'Пасьянс 4',
                         'images/patterns/uz25.png',
                         'algorithm'
                     );

INSERT INTO patterns (
                         name,
                         link,
                         algorithm
                     )
                     VALUES (
                         'Мезон',
                         'images/patterns/uz26.png',
                         'algorithm'
                     );

INSERT INTO patterns (
                         name,
                         link,
                         algorithm
                     )
                     VALUES (
                         'Куб в кубе',
                         'images/patterns/uz27.png',
                         'algorithm'
                     );

INSERT INTO patterns (
                         name,
                         link,
                         algorithm
                     )
                     VALUES (
                         'Кубик в кубе в кубе',
                         'images/patterns/uz28.png',
                         'algorithm'
                     );

INSERT INTO patterns (
                         name,
                         link,
                         algorithm
                     )
                     VALUES (
                         'Кольца',
                         'images/patterns/uz30.png',
                         'algorithm'
                     );

INSERT INTO patterns (
                         name,
                         link,
                         algorithm
                     )
                     VALUES (
                         'Змея',
                         'images/patterns/uz31.png',
                         'algorithm'
                     );

INSERT INTO patterns (
                         name,
                         link,
                         algorithm
                     )
                     VALUES (
                         'Кольца 2 с мезоном',
                         'images/patterns/uz32.png',
                         'algorithm'
                     );

INSERT INTO patterns (
                         name,
                         link,
                         algorithm
                     )
                     VALUES (
                         'Червяк',
                         'images/patterns/uz33.png',
                         'algorithm'
                     );

INSERT INTO patterns (
                         name,
                         link,
                         algorithm
                     )
                     VALUES (
                         'Рыбки',
                         'images/patterns/uz35.png',
                         'algorithm'
                     );

INSERT INTO patterns (
                         name,
                         link,
                         algorithm
                     )
                     VALUES (
                         'Уголки',
                         'images/patterns/uz36.png',
                         'algorithm'
                     );

INSERT INTO patterns (
                         name,
                         link,
                         algorithm
                     )
                     VALUES (
                         'Уголки второго порядка',
                         'images/patterns/uz37.png',
                         'algorithm'
                     );

INSERT INTO patterns (
                         name,
                         link,
                         algorithm
                     )
                     VALUES (
                         'Вишни',
                         'images/patterns/uz39.png',
                         'algorithm'
                     );

INSERT INTO patterns (
                         name,
                         link,
                         algorithm
                     )
                     VALUES (
                         'Ракета',
                         'images/patterns/uz42.png',
                         'algorithm'
                     );

INSERT INTO patterns (
                         name,
                         link,
                         algorithm
                     )
                     VALUES (
                         'Ракета второго порядка',
                         'images/patterns/uz43.png',
                         'algorithm'
                     );

INSERT INTO patterns (
                         name,
                         link,
                         algorithm
                     )
                     VALUES (
                         'Реверс',
                         'images/patterns/uz45.png',
                         'algorithm'
                     );


COMMIT TRANSACTION;
PRAGMA foreign_keys = on;

"""

# Выполнение SQL-сценария
cursor.executescript(sql_script)

# Закрытие соединения
connection.close()