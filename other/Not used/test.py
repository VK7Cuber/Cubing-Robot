# import sqlite3
# # -*- coding: utf-8 -*-
#
# # Создаем или подключаемся к базе данных
# connection = sqlite3.connect('CFOP_algorithms_data.sqlite')  # Название вашей базы данных
# cursor = connection.cursor()
#
# # Ваш SQL-код в виде строки
# sql_script = """
#
# --
# -- File generated with SQLiteStudio v3.4.4 on Ср фев 19 00:54:33 2025
# --
# -- Text encoding used: UTF-8
# --
# PRAGMA foreign_keys = off;
# BEGIN TRANSACTION;
#
# -- Table: Algorithms
# DROP TABLE IF EXISTS Algorithms;
#
# CREATE TABLE IF NOT EXISTS Algorithms (
#     id             INTEGER,
#     step           TEXT,
#     name           TEXT,
#     algorithm      TEXT,
#     repeat_to_make TEXT
# );
#
# INSERT INTO Algorithms (
#                            id,
#                            step,
#                            name,
#                            algorithm,
#                            repeat_to_make
#                        )
#                        VALUES (
#                            0,
#                            'F2L',
#                            'Трёхходовка',
#                            'R U R''',
#                            '3'
#                        );
#
# INSERT INTO Algorithms (
#                            id,
#                            step,
#                            name,
#                            algorithm,
#                            repeat_to_make
#                        )
#                        VALUES (
#                            1,
#                            'F2L',
#                            'Пара',
#                            'U R U'' R''',
#                            '5'
#                        );
#
# INSERT INTO Algorithms (
#                            id,
#                            step,
#                            name,
#                            algorithm,
#                            repeat_to_make
#                        )
#                        VALUES (
#                            2,
#                            'F2L',
#                            'Пара через фронт',
#                            'R'' F R F''',
#                            '5'
#                        );
#
# INSERT INTO Algorithms (
#                            id,
#                            step,
#                            name,
#                            algorithm,
#                            repeat_to_make
#                        )
#                        VALUES (
#                            3,
#                            'OLL',
#                            'Глаза',
#                            'R2 D'' R U2 R'' D R U2 R',
#                            '2'
#                        );
#
# INSERT INTO Algorithms (
#                            id,
#                            step,
#                            name,
#                            algorithm,
#                            repeat_to_make
#                        )
#                        VALUES (
#                            4,
#                            'OLL',
#                            'Уши',
#                            'L F R'' F'' L'' F R F''',
#                            '3'
#                        );
#
# INSERT INTO Algorithms (
#                            id,
#                            step,
#                            name,
#                            algorithm,
#                            repeat_to_make
#                        )
#                        VALUES (
#                            5,
#                            'OLL',
#                            'Вертолёт',
#                            'R U2 R2 U'' R2 U'' R2 U2 R',
#                            '1'
#                        );
#
# INSERT INTO Algorithms (
#                            id,
#                            step,
#                            name,
#                            algorithm,
#                            repeat_to_make
#                        )
#                        VALUES (
#                            6,
#                            'OLL',
#                            'Восьмёрка',
#                            'F'' L F R'' F'' L'' F R',
#                            '2'
#                        );
#
# INSERT INTO Algorithms (
#                            id,
#                            step,
#                            name,
#                            algorithm,
#                            repeat_to_make
#                        )
#                        VALUES (
#                            7,
#                            'OLL',
#                            'Двойные глаза',
#                            'R U2 R'' U'' R U R'' U'' R U'' R'' U''',
#                            '1'
#                        );
#
# INSERT INTO Algorithms (
#                            id,
#                            step,
#                            name,
#                            algorithm,
#                            repeat_to_make
#                        )
#                        VALUES (
#                            8,
#                            'OLL',
#                            'Рыбка',
#                            'R U R'' U R U2 R''',
#                            '5'
#                        );
#
# INSERT INTO Algorithms (
#                            id,
#                            step,
#                            name,
#                            algorithm,
#                            repeat_to_make
#                        )
#                        VALUES (
#                            9,
#                            'OLL',
#                            'Буква "Н"',
#                            'R U R'' U'' R'' L F R F'' L''',
#                            '2'
#                        );
#
# INSERT INTO Algorithms (
#                            id,
#                            step,
#                            name,
#                            algorithm,
#                            repeat_to_make
#                        )
#                        VALUES (
#                            10,
#                            'OLL',
#                            'Буква "Т"',
#                            'F R U R'' U'' F''',
#                            '5'
#                        );
#
# INSERT INTO Algorithms (
#                            id,
#                            step,
#                            name,
#                            algorithm,
#                            repeat_to_make
#                        )
#                        VALUES (
#                            11,
#                            'OLL',
#                            'Галстук',
#                            'F R U'' R'' U'' R U R'' F''',
#                            '3'
#                        );
#
# INSERT INTO Algorithms (
#                            id,
#                            step,
#                            name,
#                            algorithm,
#                            repeat_to_make
#                        )
#                        VALUES (
#                            12,
#                            'OLL',
#                            'Буква "М"',
#                            'R U R'' U R U'' R'' U'' R'' F R F''',
#                            '5'
#                        );
#
# INSERT INTO Algorithms (
#                            id,
#                            step,
#                            name,
#                            algorithm,
#                            repeat_to_make
#                        )
#                        VALUES (
#                            13,
#                            'PLL',
#                            'T-Perm',
#                            'R U R'' U'' R'' F R2 U'' R'' U'' R U R'' F''',
#                            '1'
#                        );
#
# INSERT INTO Algorithms (
#                            id,
#                            step,
#                            name,
#                            algorithm,
#                            repeat_to_make
#                        )
#                        VALUES (
#                            14,
#                            'PLL',
#                            'F-Perm',
#                            'R'' U'' F'' R U R'' U'' R'' F R2 U'' R'' U'' R U R'' U R',
#                            '1'
#                        );
#
# INSERT INTO Algorithms (
#                            id,
#                            step,
#                            name,
#                            algorithm,
#                            repeat_to_make
#                        )
#                        VALUES (
#                            15,
#                            'PLL',
#                            'Y-Perm',
#                            'F R U'' R'' U'' R U R'' F'' F R U R'' U'' F''',
#                            '1'
#                        );
#
#
# COMMIT TRANSACTION;
# PRAGMA foreign_keys = on;
#
#
#
# """
#
# # Выполнение SQL-сценария
# cursor.executescript(sql_script)
#
# # Закрытие соединения
# connection.close()
# # import sqlite3
# # from sqlite3 import *
# #
# # data = sqlite3.connect("CFOP_algorithms_database.sqlite")
# # cur = data.cursor()
# # query = '''
# # CREATE TABLE IF NOT EXISTS Algorithms (
# # id INTEGER,
# # step TEXT,
# # name TEXT,
# # algorithm TEXT
# # )
# # '''
# # result = cur.execute(query)
# #
# # data.close()
