import copy
import sqlite3
import threading

from setting import BASE

connection = sqlite3.connect(BASE)


class RecordNotFoundException(Exception):
    def __init__(self, message):
        super().__init__(f'Record not found: {message}')


class DbCommitException(Exception):
    def __init__(self, message):
        super().__init__(f'Db commit error: {message}')


class DbUpdateException(Exception):
    def __init__(self, message):
        super().__init__(f'Db update error: {message}')


class DbDeleteException(Exception):
    def __init__(self, message):
        super().__init__(f'Db delete error: {message}')


class PersonMapper:
    """
    Паттерн DATA MAPPER
    Слой преобразования данных
    """

    def __init__(self, connection):
        self.connection = connection
        self.cursor = connection.cursor()

    # CRUD
    # создание записей
    def insert(self, person):
        statement = f"INSERT INTO PERSON (FIRSTNAME, LASTNAME, USER_TYPE, EMAIL, PASSWORD) VALUES (?, ?, ?, ?, ?)"
        self.cursor.execute(statement, (person.firstname, person.lastname, person.user_type, person.email, person.password))
        try:
            self.connection.commit()
        except Exception as e:
            raise DbCommitException(e.args)

    # чтение записей по id
    def find_by_id(self, id):
        statement = f"SELECT id, lastname, firstname, user_type, email, password FROM PERSON WHERE ID=?"
        self.cursor.execute(statement, (id,))
        result = self.cursor.fetchone()
        if result:
            return Person(*result)
        else:
            raise RecordNotFoundException(f'record with id={id} not found')

    # чтение всех записей
    def get(self):
        statement = f"SELECT id, lastname, firstname, user_type, email, password FROM PERSON ORDER BY id "
        self.cursor.execute(statement)
        result = self.cursor.fetchall()
        if result:
            return result
        else:
            raise RecordNotFoundException(f'no users')
        
    # редактирование записей
    def update(self, person):
        statement = f"UPDATE PERSON SET FIRSTNAME=?, LASTNAME=?, USER_TYPE=? WHERE ID=?"
        self.cursor.execute(statement, (person.firstname, person.lastname, person.user_type, person.id))
        try:
            self.connection.commit()
        except Exception as e:
            raise DbUpdateException(e.args)
        
    # удаление записей
    def delete(self, id):
        statement = f"DELETE FROM PERSON WHERE ID=?"
        self.cursor.execute(statement, (id,))
        try:
            self.connection.commit()
        except Exception as e:
            raise DbDeleteException(e.args)


class CategoryMapper:
    """
        Паттерн DATA MAPPER
        Слой преобразования данных
        """

    def __init__(self, connection):
        self.connection = connection
        self.cursor = connection.cursor()

    # CRUD
    # создание записей
    def insert(self, category):
        statement = f"INSERT INTO CATEGORY (NAME) VALUES (?)"
        self.cursor.execute(statement, (category.name, ))
        try:
            self.connection.commit()
        except Exception as e:
            raise DbCommitException(e.args)

    # чтение записей по id
    def find_by_id(self, id):
        statement = f"SELECT id, name FROM CATEGORY WHERE ID=?"
        self.cursor.execute(statement, (id, ))
        result = self.cursor.fetchone()
        if result:
            return result
        else:
            raise RecordNotFoundException(f'record with id={id} not found')

    # чтение всех записей
    def get(self):
        statement = f"SELECT name FROM CATEGORY ORDER BY id "
        self.cursor.execute(statement)
        result = self.cursor.fetchall()
        if result:
            return result
        else:
            raise RecordNotFoundException(f'no category')

    # редактирование записей
    def update(self, category):
        statement = f"UPDATE CATEGORY SET NAME=? WHERE ID=?"
        self.cursor.execute(statement, (category.name))
        try:
            self.connection.commit()
        except Exception as e:
            raise DbUpdateException(e.args)

    # удаление записей
    def delete(self, category):
        statement = f"DELETE FROM CATEGORY WHERE ID=?"
        self.cursor.execute(statement, (category.id,))
        try:
            self.connection.commit()
        except Exception as e:
            raise DbDeleteException(e.args)


class CourseMapper:
    """
        Паттерн DATA MAPPER
        Слой преобразования данных
        """

    def __init__(self, connection):
        self.connection = connection
        self.cursor = connection.cursor()

    # CRUD
    # создание записей
    def insert(self, course):
        statement = f"INSERT INTO COURSE " \
                    f"(CATEGORY, NAME, FORM_COURSE, TYPE_COURSE) " \
                    f"VALUES (?, ?, ?, ?)"
        self.cursor.execute(statement, (course.category, course.name, course.form_course, course.type_course))
        try:
            self.connection.commit()
        except Exception as e:
            raise DbCommitException(e.args)

    # чтение записей по id
    def find_by_id(self, id):
        statement = f"SELECT CATEGORY, NAME, FORM_COURSE, TYPE_COURSE FROM COURSE WHERE ID=?"
        self.cursor.execute(statement, (id,))
        result = self.cursor.fetchone()
        if result:
            return Course(*result)
        else:
            raise RecordNotFoundException(f'record with id={id} not found')

    # чтение всех записей
    def get(self):
        statement = f"SELECT category, name, form_course, type_course FROM COURSE ORDER BY id "
        self.cursor.execute(statement)
        result = self.cursor.fetchall()
        if result:
            return result
        else:
            raise RecordNotFoundException(f'no course')

    # редактирование записей
    def update(self, course):
        statement = f"UPDATE COURSE SET CATEGORY=?, NAME=?, FORM_COURSE=?, TYPE_COURSE=?"
        self.cursor.execute(statement, (course.category, course.name, course.form_course, course.type_course))
        try:
            self.connection.commit()
        except Exception as e:
            raise DbUpdateException(e.args)

    # удаление записей
    def delete(self, course):
        statement = f"DELETE FROM COURSE WHERE ID=?"
        self.cursor.execute(statement, (course.id,))
        try:
            self.connection.commit()
        except Exception as e:
            raise DbDeleteException(e.args)


class MapperRegistry:
    @staticmethod
    def get_mapper(obj):
        if isinstance(obj, Person):
            return PersonMapper(connection)
        elif isinstance(obj, Category):
            return CategoryMapper(connection)
        elif isinstance(obj, Course):
            return CourseMapper(connection)


class GetMapper:
    @staticmethod
    def get_mapper_type(type_):
        if type_ == 'Person':
            return PersonMapper(connection)
        elif type_ == 'Category':
            return CategoryMapper(connection)
        elif type_ == 'Course':
            return CourseMapper(connection)


class UnitOfWork:
    """
    Паттерн UNIT OF WORK
    """
    # Работает с конкретным потоком
    current = threading.local()

    def __init__(self):
        self.new_objects = []
        self.dirty_objects = []
        self.removed_objects = []
        self.unit_of_work = []

    def register_new(self, obj):
        self.new_objects.append(obj)

    def register_dirty(self, obj):
        self.dirty_objects.append(obj)

    def register_removed(self, obj):
        self.removed_objects.append(obj)

    def commit(self):
        self.insert_new()
        self.update_dirty()
        self.delete_removed()

    def insert_new(self):
        for obj in self.new_objects:
            MapperRegistry.get_mapper(obj).insert(obj)

    def update_dirty(self):
        for obj in self.dirty_objects:
            MapperRegistry.get_mapper(obj).update(obj)

    def delete_removed(self):
        for obj in self.removed_objects:
            MapperRegistry.get_mapper(obj).delete(obj)

    @staticmethod
    def new_current():
        # создание экземпляра UnitOfWork
        __class__.set_current(UnitOfWork())

    @classmethod
    def set_current(cls, unit_of_work):
        cls.current.unit_of_work = unit_of_work


    @classmethod
    def get_current(cls):
        return cls.current.unit_of_work


class DomainObject:

    def mark_new(self):
        UnitOfWork.get_current().register_new(self)

    def mark_dirty(self):
        UnitOfWork.get_current().register_dirty(self)

    def mark_removed(self):
        UnitOfWork.get_current().register_removed(self)


class Person(DomainObject):
    def __init__(self, id, lastname, firstname, user_type, email, password):
        self.id = id
        self.lastname = lastname
        self.firstname = firstname
        self.user_type = user_type
        self.email = email
        self.password = password


class Category(DomainObject):
    def __init__(self, name):
        self.name = name


class Course(DomainObject):
    def __init__(self, category, name, form_course, type_course):
        self.category = category
        self.name = name
        self.form_course = form_course
        self.type_course = type_course


class InteractiveCourse(Course):
    pass


class RecordCourse(Course):
    pass


class CourseFactory:
    types = {
        'interactive': InteractiveCourse,
        'record': RecordCourse
    }

    @classmethod
    def create(cls, type_, *args):
        return cls.types[type_](*args)


class MainFactory:

    types = {
        'Person': Person,
        'Category': Category,
        'Course': Course,
    }


class TrainingSite:

    @staticmethod
    def create(type_, *args):
        UnitOfWork.new_current()
        obj = MainFactory.types[type_](*args)
        obj.mark_new()
        UnitOfWork.get_current().commit()

    @staticmethod
    def find_by_id(type_, id):
        return GetMapper.get_mapper_type(type_).find_by_id(id)

    @staticmethod
    def get(type_):
        return GetMapper.get_mapper_type(type_).get()

    @staticmethod
    def update(type_, *args):
        UnitOfWork.new_current()
        obj = MainFactory.types[type_](*args)
        obj.mark_dirty()
        UnitOfWork.get_current().commit()

    @staticmethod
    def get_copy(name, *args):
        pass

    @staticmethod
    def delete(type_, id):
        pass


if __name__ == '__main__':
    site = TrainingSite
    site.create('Person', None, 'Fedorov', 'Fedor', 'student', 'email@email.ru', '123456789')
    site.create('Category', 'new')
    site.create('Course', 'C++', 'C++ - начальный курс', 'online', 'webinar')

    print(site.get('Person'))
    print(site.get('Category'))
    print(site.get('Course'))

    print(site.find_by_id('Person', 1).firstname)
    print(site.find_by_id('Category', 1))
    print(site.find_by_id('Course', 1).name)

    site.update('Person', 1, 'Ivanov_new', 'Ivan_new', 'user', 'email@email.ru', '123456789')
    site.update('Category', 'C#')
    site.update('Course', 'C++', 'C++ - начальный курс new', 'online', 'webinar')
    #
    # site.delete('Person', 5)


