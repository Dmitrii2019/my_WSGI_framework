import copy


class User:
    def __init__(self, type_, name, email, password):
        self.type_ = type_
        self.name = name
        self.email = email
        self.password = password
        print('Пользователь создан в User')


class Teacher(User):
    def __init__(self, type_, name, email, password):
        super().__init__(type_, name, email, password)
        self.type_ = type_
        print('Пользователь создан в виде учителя')


class Student(User):
    def __init__(self, type_, name, email, password):
        super().__init__(type_, name, email, password)
        self.type_ = type_
        print('Пользователь создан в виде студента')


class SimpleFactory:
    # Фабричный метод
    def __init__(self, types=None):
        self.types = types or {}


class UserFactory:
    types = {
        'user': User,
        'student': Student,
        'teacher': Teacher
    }

    @classmethod
    def create(cls, type_, name, email, password):
        return cls.types[type_](type_, name, email, password)


class Category:
    # реестр?
    auto_id = 0

    def __init__(self, name, category):
        self.id = Category.auto_id
        Category.auto_id += 1
        self.name = name
        self.category = category
        self.courses = []

    def course_count(self):
        result = len(self.courses)
        if self.category:
            result += self.category.course_count()
        return result


class Course:

    def __init__(self, name, category):
        self.name = name
        self.category = category
        self.category.courses.append(self)

    def clone(self):
        """Clone a registered object and update inner attributes dictionary"""
        return copy.deepcopy(self)


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
    def create(cls, type_, name, category):
        return cls.types[type_](name, category)


class TrainingSite:
    # Интерфейс
    def __init__(self):
        self.user = []
        self.teachers = []
        self.students = []
        self.courses = []
        self.categories = []

    def create_user(self, type_,  name, email, password):
        return UserFactory.types[type_](type_, name, email, password)

    def get_user(self):
        for item in self.user:
            if item.name:
                return item.name
        return None

    def create_category(self, name, category=None):
        return Category(name, category)

    def find_category_by_id(self, id):
        for item in self.categories:
            print('item', item.id)
            if item.id == id:
                return item
        raise Exception(f'Нет категории с id = {id}')

    def create_course(self, type_, name, category):
        return CourseFactory.create(type_, name, category)

    def get_course(self, name) -> Course:
        for item in self.courses:
            if item.name == name:
                return item
        return None
