import sqlite3
# -*- coding: utf-8 -*-

# Создаем или подключаемся к базе данных
connection = sqlite3.connect('Algorithms.sqlite')  # Название вашей базы данных
cursor = connection.cursor()

# Ваш SQL-код в виде строки
sql_script = """

-- Create the database
CREATE DATABASE IF NOT EXISTS CFOP_Algorithms_DB;

-- Use the created database
USE CFOP_Algorithms_DB;

-- Create a table for storing CFOP algorithms
CREATE TABLE IF NOT EXISTS Algorithms (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    notation VARCHAR(255) NOT NULL,
    difficulty_level ENUM('Beginner', 'Intermediate', 'Advanced') NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Insert CFOP algorithms into the table
INSERT INTO Algorithms (name, description, notation, difficulty_level)
VALUES
    -- Cross Algorithms
    ('Cross', 'Forming a cross on the first layer.', 'F R U R\' U\' F\'', 'Beginner'),

    -- F2L Algorithms
    ('F2L - Pairing', 'Pairing edge and corner pieces.', 'U R U\' R\' U\' F\' U F', 'Intermediate'),
    
    ('F2L - Insertion', 'Inserting the paired F2L pieces.', 'R U R\' U\'', 'Intermediate'),
    ('F2L - Backward Pairing', 'Pairing in the back before insertion.', 'U\' L F U L\' U L F\' L\'', 'Intermediate'),
    ('F2L - Edge-Last Insertion', 'Inserts edge last after corner.', 'R U R\' U\' L\' U\' L', 'Intermediate'),
    ('F2L - Corner-First Insertion', 'Inserts corner first for advanced cases.', 'U R U R\' U R U\' R\'', 'Intermediate'),
    ('F2L - 3 Edge Case', 'Solves F2L when two edges are solved.', 'U R U\' R\' U\' F\' U F', 'Intermediate'),
    
    -- Additional F2L Cases
    ('F2L - Two Edge Case', 'Fixes two edges being solved but one misplaced corner.', 'U R U\' R\' U2 R U\' R\'', 'Intermediate'),
    ('F2L - 4 Pieces Solved', 'When all edges are in position except the last corner.', 'U R U\' R\' U2 R U2 R\'', 'Advanced'),
    ('F2L - No Edge Case', 'All F2L corners solved with no edge to align.', 'U R U\' R\' U R U\' R\'', 'Intermediate'),

    -- OLL Algorithms
    ('OLL - Dot Case', 'All edges and corners incorrectly oriented.', 'F R U R\' U\' F\' F U R U\' R\' F', 'Advanced'),
    ('OLL - Cross', 'Creating a cross on the last layer.', 'F R U R\' U\' F\'', 'Advanced'),
    ('OLL - L Shape', 'Creating an L shape on the top face.', 'F U R U\' R\' F\'', 'Advanced'),
    ('OLL - Headlights', 'Two adjacent corners oriented.', 'R2 D\' R U2 R\' D R U2 R', 'Advanced'),
    ('OLL - Sune', 'One corner oriented and adjacent edges.', 'R U R\' U R U2 R\'', 'Advanced'),
    ('OLL - Anti-Sune', 'One corner oriented opposite of Sune.', 'R\' U\' R U\' R\' U2 R', 'Advanced'),
    ('OLL - Pi Case', 'Creating a Pi shape with edges.', 'R U R\' U R U R\' U\' R U\' R\'', 'Advanced'),
    ('OLL - T Shape', 'Creating a T shape with edges.', 'R U R\' U R U2 R\' U2 R', 'Advanced'),
    
    -- More OLL Cases
    ('OLL - Bow Tie', 'Bow-tie shape with edges.', 'R U R\' U R U2 R\' U2 R', 'Advanced'),
    ('OLL - 2 Edges Oriented', 'Two edges oriented parallel.', 'F R U R\' U\' F\' U R U\' R\'', 'Advanced'),
    ('OLL - Edge Pair', 'Two edges oriented.', 'F U R U\' R\' F\' U R U\'', 'Advanced'),
    ('OLL - 4 Edges Oriented', 'All edges oriented correctly.', 'R U R\' U R U R\' U\' R U\' R\'', 'Advanced'),
    
    -- PLL Algorithms
    ('PLL - T Perm', 'Switching two adjacent corners and one adjacent edge.', 'R U R\' U\' R\' F R F\'', 'Advanced'),
    
    ('PLL - U Perm', 'Switching two opposite corners and one pair of edges.', 'F R U\' R\' D R U R\' D\' R F\'', 'Advanced'),
    ('PLL - J Perm', 'Switching two corners and their adjacent edges.', 'L F\' L B2 L\' F L B2 L2', 'Advanced'),
    ('PLL - H Perm', 'Swapping opposite edges.', 'M2 U M2 U2 M2 U M2', 'Advanced'),
    ('PLL - Z Perm', 'Swapping adjacent edges.', 'M U M U2 M\' U M U2 M\'', 'Advanced'),

    -- Additional PLL Cases
    ('PLL - A Perm (A1)', 'Switching two opposite edges and two adjacent corners.', 'x\' R U\' R D2 R\' U R D2 R2 x', 'Advanced'),
    ('PLL - A Perm (A2)', 'Similar to A1 but with a different orientation.', 'x R\' U R D2 R\' U\' R D2 R2 x\'', 'Advanced'),
    ('PLL - E Perm', 'All edges are in place; two adjacent edges swap.', 'M2 U M2 U M\' U2 M2 U2 M\'', 'Advanced'),
    ('PLL - Y Perm', 'Swapping two edges and two adjacent corners.', 'R U R\' U\' R\' F R2 U R\' U\' R U R\' F\'', 'Advanced'),
    ('PLL - F Perm', 'Swapping two adjacent corners and two opposite edges.', 'x R U\' R D2 R\' U R D2 R\' x\'', 'Advanced'),
    ('PLL - V Perm', 'Swapping two adjacent edges and two opposite corners.', 'R U R\' U R U R\' U\' R U\' R\'', 'Advanced'),

    -- Last Layer Algorithms
    ('Last Layer - Full OLL 2-Look', 'Two-look OLL for quick completion.', 'F R U R\' U\' F\' F U R U\' R\' F', 'Intermediate'),
    ('Last Layer - Full PLL 2-Look', 'Two-look PLL for better control.', 'M2 U M2 U M\' U2 M2 U2 M\'', 'Intermediate'),

    -- Combination Algorithms for Advanced Solving
    ('G Perm - G1', 'One of the G permutations.', '(R\' U2 R \') F (R\' U R) U (R\' U R) F\'', 'Advanced'),
    ('G Perm - G2', 'Another G permutation.', '(R U2 R\') F (R U R\') U\' (R U\' R) F\'', 'Advanced'),
    ('F2L - Combination Edge Cases', 'Combining edge orientations for efficient solves.', 'U R U\' R\' F R U R\' F\'', 'Advanced')
;

"""

# Выполнение SQL-сценария
cursor.executescript(sql_script)

# Закрытие соединения
connection.close()