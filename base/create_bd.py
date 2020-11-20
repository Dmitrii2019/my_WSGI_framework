import sqlite3

from setting import BASE

connection = sqlite3.connect(BASE)
cursor = connection.cursor()

# удаляем таблицу
# Создание таблицы PERSON
# Вставляем данные в таблицу
cursor.executescript("""
DROP TABLE IF EXISTS PERSON;

CREATE TABLE PERSON (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL UNIQUE,
 lastname VARCHAR (32), firstname VARCHAR (32), user_type VARCHAR (32), COURSE VARCHAR (32), email VARCHAR (32), password VARCHAR (32));

INSERT INTO PERSON (lastname, firstname, user_type, course, email, password) VALUES
 ('Ivanov', 'Ivan', 'user', 'python для новичков', 'user_mail@mail.ru', '123456');
 INSERT INTO PERSON (lastname, firstname, user_type, course, email, password) VALUES
 ('Borisov', 'Boris', 'student', 'java для новичков', 'student_mail@mail.ru', '1234562');
 INSERT INTO PERSON (lastname, firstname, user_type, course, email, password) VALUES
 ('Romanov', 'Roman', 'teacher', 'javascript для новичков', 'teacher_mail@mail.ru', '1234562');
""")

# Сохраняем изменения
connection.commit()

cursor.executescript("""
DROP TABLE IF EXISTS CATEGORY;

CREATE TABLE CATEGORY (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL UNIQUE,
 name VARCHAR (32), course VARCHAR (32));

INSERT INTO CATEGORY (name, course) VALUES
 ('python', 'python для новичков');
 INSERT INTO CATEGORY (name, course) VALUES
 ('java', 'java для новичков');
 INSERT INTO CATEGORY (name, course) VALUES
 ('javascript', 'javascript для новичков');
""")

# Сохраняем изменения
connection.commit()

cursor.executescript("""
DROP TABLE IF EXISTS COURSE;

CREATE TABLE COURSE (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL UNIQUE,
 name VARCHAR (32), form_course VARCHAR (32), type_course VARCHAR (32));

 INSERT INTO COURSE (name, form_course, type_course) VALUES
 ('python для профи', 'offline', 'address');
 INSERT INTO COURSE (name, form_course, type_course) VALUES
 ('java для профи', 'online', 'webinar');
 INSERT INTO COURSE (name, form_course, type_course) VALUES
 ('javascript для профи', 'online', 'webinar');
""")

# Сохраняем изменения
connection.commit()
