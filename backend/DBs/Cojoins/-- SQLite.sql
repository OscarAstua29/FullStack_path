-- SQLite

-- CREATE TABLES

-- CREATE TABLE books (
--     id INTEGER PRIMARY KEY AUTOINCREMENT,
--     name VARCHAR(25) NOT NULL,
--     author_id INT REFERENCES authors(id)
-- );

-- create table authors(
--   id INTEGER PRIMARY KEY AUTOINCREMENT,
--   name VARCHAR(25)NOT NULL

-- );

-- create table customers(
--   id INTEGER PRIMARY KEY AUTOINCREMENT,
--   name VARCHAR(25)NOT NULL,
--   mail VARCHAR(50)NOT NULL

-- );

-- create table rents(
--   id INTEGER PRIMARY KEY AUTOINCREMENT,
--   book_id INT REFERENCES books(id),
--   customer_id INT REFERENCES customers(id),
--   state VARCHAR(15) NOT NULL
-- );
-- 
-- ADD DATA

-- INSERT INTO authors (name)
-- VALUES 
--     ('Miguel de Cervantes'),
--     ('Dante Alighieri'),
--     ('Takehiko Inoue'),
--     ('Akira Toriyama'),
--     ('Walt Disney');

-- INSERT INTO books (name, author_id)
-- VALUES 
--     ('Don Quijote', 1),
--     ('La Divina Comedia', 2),
--     ('Vagabond 1-3', 3),
--     ('Dragon Ball 1', 4),
--     ('The Book of the 5 Rings', NULL);

-- INSERT INTO customers (name, mail)
-- VALUES 
--     ('John Doe', 'j.doe@email.com'),
--     ('Jane Doe', 'jane@doe.com'),
--     ('Luke Skywalker', 'darth.son@email.com');


-- INSERT INTO rents (book_id, customer_id, state)
-- VALUES 
--     ( 1, 2, 'Returned'),
--     ( 2, 2, 'Returned'),
--     ( 1, 1, 'Ontime'),
--     ( 3, 1, 'Ontime'),
--     ( 2, 2, 'Overdue');



-- DROP TABLE authors;
-- DROP TABLE books;
-- DROP TABLE customes;
-- DROP TABLE rents;j.doe@email.com

-- 1

-- SELECT books.name  AS Book_Title, authors.name AS Author_Name
-- FROM books
-- INNER JOIN authors ON books.author_id = authors.id;


-- 2

-- SELECT books.name  AS Book_Title
-- FROM books
-- LEFT JOIN authors ON books.author_id = authors.id
-- where authors.id is null;

-- 3

-- SELECT authors.name  AS author
-- FROM authors
-- left JOIN books ON authors.id = books.author_id
-- where books.id is null;

-- 4

-- SELECT DISTINCT books.name AS book_rented (para que no se repitan valores)
-- FROM rents
-- left join books ON rents.book_id = books.id;

--5 

-- select books.name as book_not_rented
-- FROM books
-- WHERE NOT EXISTS (SELECT rents.book_id FROM rents WHERE rents.book_id = books.id);

--6 

-- Select customers.name as customer_without_rent
-- FROM customers
-- WHERE NOT EXISTS (SELECT rents.customer_id FROM rents WHERE rents.customer_id = customers.id);

-- 7


-- select books.name as books_rented_overdue
-- FROM books
-- WHERE (SELECT rents.book_id FROM rents WHERE rents.book_id = books.id AND rents.state = 'Overdue');
