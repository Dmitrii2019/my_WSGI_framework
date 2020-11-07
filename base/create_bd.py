import sqlite3
import os.path

path = os.getcwd()
connection = sqlite3.connect(f'{path}/database.db')
cursor = connection.cursor()

# удаляем таблицу
# Создание таблицы PERSON
# Вставляем данные в таблицу
cursor.executescript("""
DROP TABLE IF EXISTS PERSON;

CREATE TABLE PERSON (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL UNIQUE,
 lastname VARCHAR (32), firstname VARCHAR (32), user_type VARCHAR (32), email VARCHAR (32), password VARCHAR (32));

INSERT INTO PERSON (lastname, firstname, user_type, email, password) VALUES
 ('Ivanov', 'Ivan', 'user', 'user_mail@mail.ru', '123456');
 INSERT INTO PERSON (lastname, firstname, user_type, email, password) VALUES
 ('Borisov', 'Boris', 'student', 'student_mail@mail.ru', '1234562');
 INSERT INTO PERSON (lastname, firstname, user_type, email, password) VALUES
 ('Romanov', 'Roman', 'teacher', 'teacher_mail@mail.ru', '1234562');
""")

# Сохраняем изменения
connection.commit()

cursor.executescript("""
DROP TABLE IF EXISTS CATEGORY;

CREATE TABLE CATEGORY (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL UNIQUE,
 name VARCHAR (32));

INSERT INTO CATEGORY (name) VALUES
 ('python');
 INSERT INTO CATEGORY (name) VALUES
 ('java');
 INSERT INTO CATEGORY (name) VALUES
 ('javascript');
""")

# Сохраняем изменения
connection.commit()

cursor.executescript("""
DROP TABLE IF EXISTS COURSE;

CREATE TABLE COURSE (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL UNIQUE,
 category VARCHAR (32), name VARCHAR (32), form_course VARCHAR (32), type_course VARCHAR (32));

 INSERT INTO COURSE (category, name, form_course, type_course) VALUES
 ('python', 'курсы python для новичков', 'offline', 'address');
 INSERT INTO COURSE (category, name, form_course, type_course) VALUES
 ('java', 'курсы java для новичков', 'online', 'webinar');
 INSERT INTO COURSE (category, name, form_course, type_course) VALUES
 ('javascript', 'курсы javascript для новичков', 'online', 'webinar');
""")

# Сохраняем изменения
connection.commit()

# statement = "INSERT INTO person (lastname, firstname, user_type, email, password) VALUES (?, ?, ?, ?, ?)"
# cursor.execute(statement, ('last_name', 'first_name', 'учитель', 'mail1@mail.ru', 65432))
# connection.commit()
#
# statement = f"SELECT *  FROM PERSON WHERE IDPERSON=?"
# id_person = 2
# cursor.execute(statement, (id_person,))
# result = cursor.fetchone()
# # print(result)

