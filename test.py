import sqlite3
# -*- coding: utf-8 -*-

# Создаем или подключаемся к базе данных
connection = sqlite3.connect('Algorithms.sqlite')  # Название вашей базы данных
cursor = connection.cursor()

# Ваш SQL-код в виде строки
sql_script = """

--
-- File generated with SQLiteStudio v3.4.4 on Вс фев 16 22:38:01 2025
--
-- Text encoding used: UTF-8
--
PRAGMA foreign_keys = off;
BEGIN TRANSACTION;

-- Table: Algorithms
DROP TABLE IF EXISTS Algorithms;

CREATE TABLE IF NOT EXISTS Algorithms (
    id        INTEGER,
    algorithm TEXT
);

INSERT INTO Algorithms (
                           id,
                           algorithm
                       )
                       VALUES (
                           0,
                           'U R U'' R'' U'' F'' U F'
                       );

INSERT INTO Algorithms (
                           id,
                           algorithm
                       )
                       VALUES (
                           1,
                           'F R U R'' U'' R U R'' U'' F'' U F R U R'' U'' F'''
                       );

INSERT INTO Algorithms (
                           id,
                           algorithm
                       )
                       VALUES (
                           2,
                           'F R U R'' U'' F'''
                       );

INSERT INTO Algorithms (
                           id,
                           algorithm
                       )
                       VALUES (
                           3,
                           'F U R U'' R'' F'''
                       );

INSERT INTO Algorithms (
                           id,
                           algorithm
                       )
                       VALUES (
                           4,
                           'R U R'' U R U2 R'''
                       );

INSERT INTO Algorithms (
                           id,
                           algorithm
                       )
                       VALUES (
                           5,
                           'R U'' L'' U R'' U'' L U'
                       );

INSERT INTO Algorithms (
                           id,
                           algorithm
                       )
                       VALUES (
                           6,
                           'R F'' R'' F'
                       );


COMMIT TRANSACTION;
PRAGMA foreign_keys = on;


"""

# Выполнение SQL-сценария
cursor.executescript(sql_script)

# Закрытие соединения
connection.close()
# import sqlite3
# from sqlite3 import *
#
# data = sqlite3.connect("Base_method_algorithms_data.sqlite")
# cur = data.cursor()
# query = '''
# CREATE TABLE IF NOT EXISTS Algorithms (
# id INTEGER,
# algorithm TEXT
# )
# '''
# result = cur.execute(query)
#
# data.close()