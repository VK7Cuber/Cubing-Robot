--
-- File generated with SQLiteStudio v3.4.4 on Сб фев 8 22:02:26 2025
--
-- Text encoding used: UTF-8
--
PRAGMA foreign_keys = off;
BEGIN TRANSACTION;

-- Table: patterns
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
                         'R L'' F B'' U D'' R L'''
                     );

INSERT INTO patterns (
                         name,
                         link,
                         algorithm
                     )
                     VALUES (
                         'Шахматы',
                         'images/patterns/uz1.png',
                         'R2 L2 U2 D2 F2 B2'
                     );

INSERT INTO patterns (
                         name,
                         link,
                         algorithm
                     )
                     VALUES (
                         'Шахматы с точками',
                         'images/patterns/uz2.png',
                         'R2 L2 U2 D2 F2 B2 R L'' F B'' U D'' R L'''
                     );

INSERT INTO patterns (
                         name,
                         link,
                         algorithm
                     )
                     VALUES (
                         'Зигзаг',
                         'images/patterns/uz3.png',
                         'R L F B R L F B R L F B'
                     );

INSERT INTO patterns (
                         name,
                         link,
                         algorithm
                     )
                     VALUES (
                         'Четыре Z',
                         'images/patterns/uz4.png',
                         'R L F B R L F B R L F B U2 D2'
                     );

INSERT INTO patterns (
                         name,
                         link,
                         algorithm
                     )
                     VALUES (
                         'Крест Пламмера',
                         'images/patterns/uz6.png',
                         'B F2 D'' R2 F D B'' F D'' U F'' D'' L2 F D2 U'''
                     );

INSERT INTO patterns (
                         name,
                         link,
                         algorithm
                     )
                     VALUES (
                         'Крест Кристмана',
                         'images/patterns/uz7.png',
                         'R L2 F2 B2 U2 R2 L2 F2 B2 D2 R'
                     );

INSERT INTO patterns (
                         name,
                         link,
                         algorithm
                     )
                     VALUES (
                         'Шахматы 3-го порядка',
                         'images/patterns/uz8.png',
                         'В разработке.....'
                     );

INSERT INTO patterns (
                         name,
                         link,
                         algorithm
                     )
                     VALUES (
                         'Шахматы 6-го порядка',
                         'images/patterns/uz9.png',
                         'В разработке.....'
                     );

INSERT INTO patterns (
                         name,
                         link,
                         algorithm
                     )
                     VALUES (
                         '6 букв Н',
                         'images/patterns/uz10.png',
                         'D2 R L’ U2 D2 R L’'
                     );

INSERT INTO patterns (
                         name,
                         link,
                         algorithm
                     )
                     VALUES (
                         '6 минусов',
                         'images/patterns/uz11.png',
                         'R2 F2 R2 L2 F2 R L'
                     );

INSERT INTO patterns (
                         name,
                         link,
                         algorithm
                     )
                     VALUES (
                         'Диагональные столбики',
                         'images/patterns/uz12.png',
                         'F L D2 R'' D L2 D'' R D2 L'' F L2 F2'
                     );

INSERT INTO patterns (
                         name,
                         link,
                         algorithm
                     )
                     VALUES (
                         'Столбики с крестом',
                         'images/patterns/uz14.png',
                         'В разработке.....'
                     );

INSERT INTO patterns (
                         name,
                         link,
                         algorithm
                     )
                     VALUES (
                         'Столбики с шахматным крестом',
                         'images/patterns/uz15.png',
                         'В разработке.....'
                     );

INSERT INTO patterns (
                         name,
                         link,
                         algorithm
                     )
                     VALUES (
                         'Столбики с крышей',
                         'images/patterns/uz16.png',
                         'В разработке.....'
                     );

INSERT INTO patterns (
                         name,
                         link,
                         algorithm
                     )
                     VALUES (
                         '4 буквы П',
                         'images/patterns/uz17.png',
                         'R2 L2 U R2 L2 D2 R2 L2 D F2 B2 U’ D'
                     );

INSERT INTO patterns (
                         name,
                         link,
                         algorithm
                     )
                     VALUES (
                         '4 буквы Т',
                         'images/patterns/uz18.png',
                         'R2 L2 U R2 L2 D2 R2 L2 D F2 B2 U’ D U2'
                     );

INSERT INTO patterns (
                         name,
                         link,
                         algorithm
                     )
                     VALUES (
                         'Буквы L',
                         'images/patterns/uz19.png',
                         'L'' R'' U D L R U'' D'' F'' B'' U D'
                     );

INSERT INTO patterns (
                         name,
                         link,
                         algorithm
                     )
                     VALUES (
                         'Пасьянс 1',
                         'images/patterns/uz22.png',
                         'R'' U B2 U'' F'' U B2 U'' F R'
                     );

INSERT INTO patterns (
                         name,
                         link,
                         algorithm
                     )
                     VALUES (
                         'Пасьянс 4',
                         'images/patterns/uz25.png',
                         'R’ D U2 B U D’ R2 U’ D B D’ U2 R'
                     );

INSERT INTO patterns (
                         name,
                         link,
                         algorithm
                     )
                     VALUES (
                         'Мезон',
                         'images/patterns/uz26.png',
                         'U'' B2 U L'' F2 L U'' B2 U L'' F2 L'
                     );

INSERT INTO patterns (
                         name,
                         link,
                         algorithm
                     )
                     VALUES (
                         'Куб в кубе',
                         'images/patterns/uz27.png',
                         'U2 F2 R2 U'' L2 D B R'' B R'' B R'' D'' L2 U'''
                     );

INSERT INTO patterns (
                         name,
                         link,
                         algorithm
                     )
                     VALUES (
                         'Кубик в кубе в кубе',
                         'images/patterns/uz28.png',
                         'U'' L2 F2 D'' L'' D U2 R U'' R'' U2 R2 U F'' L'' U R'''
                     );

INSERT INTO patterns (
                         name,
                         link,
                         algorithm
                     )
                     VALUES (
                         'Кольца',
                         'images/patterns/uz30.png',
                         'R'' F2 U2 R2 B'' L2 D'' B2 R'' B2 L2 B R2 U'' R2'
                     );

INSERT INTO patterns (
                         name,
                         link,
                         algorithm
                     )
                     VALUES (
                         'Змея',
                         'images/patterns/uz31.png',
                         'R F B'' D'' F2 D B F'' R'' F2 U R2 U'' D F2 D'''
                     );

INSERT INTO patterns (
                         name,
                         link,
                         algorithm
                     )
                     VALUES (
                         'Кольца 2 с мезоном',
                         'images/patterns/uz32.png',
                         'В разработке.....'
                     );

INSERT INTO patterns (
                         name,
                         link,
                         algorithm
                     )
                     VALUES (
                         'Червяк',
                         'images/patterns/uz33.png',
                         'U B2 L D B'' F L'' D U'' L'' R F'' D2 R'''
                     );

INSERT INTO patterns (
                         name,
                         link,
                         algorithm
                     )
                     VALUES (
                         'Рыбки',
                         'images/patterns/uz35.png',
                         'U F2 U'' B'' U2 B U'' F2 U'' R'' U2 B'' U2 B R'
                     );

INSERT INTO patterns (
                         name,
                         link,
                         algorithm
                     )
                     VALUES (
                         'Уголки',
                         'images/patterns/uz36.png',
                         'F2 R2 D R2 D U F2 D'' R'' D'' F L2 F'' D R U'''
                     );

INSERT INTO patterns (
                         name,
                         link,
                         algorithm
                     )
                     VALUES (
                         'Уголки второго порядка',
                         'images/patterns/uz37.png',
                         'U L2 D F D'' B'' U L'' B2 U2 F U'' F'' U2 B'' U'''
                     );

INSERT INTO patterns (
                         name,
                         link,
                         algorithm
                     )
                     VALUES (
                         'Вишни',
                         'images/patterns/uz39.png',
                         'D F2 U'' B F'' L R'' D L2 U'' B R2 B'' U L2 U'''
                     );

INSERT INTO patterns (
                         name,
                         link,
                         algorithm
                     )
                     VALUES (
                         'Ракета',
                         'images/patterns/uz42.png',
                         'D U L2 B2 D U'' F'' U F'' R F2 R'' F D'' B2 L2 D'' U'''
                     );

INSERT INTO patterns (
                         name,
                         link,
                         algorithm
                     )
                     VALUES (
                         'Ракета второго порядка',
                         'images/patterns/uz43.png',
                         'B2 U L2 R2 D'' F'' D'' R U F2 L2 U L'' D2 L R B'' U'
                     );

INSERT INTO patterns (
                         name,
                         link,
                         algorithm
                     )
                     VALUES (
                         'Реверс',
                         'images/patterns/uz45.png',
                         'U R U2 R F2 L U2 R F'' B'' R2 D R'' L U2 F2 D2 F R2 D'
                     );


COMMIT TRANSACTION;
PRAGMA foreign_keys = on;
