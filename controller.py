from base.data_mapper import TrainingSite
from decorators.debug import debug
from setting import OK, NOT_FOUND, REDIRECT
from wavy.template import render
from wavy.utilities import Response

site = TrainingSite()


@debug
def main_view(request, method, request_params):
    title = 'Главна'
    return Response(OK, [render('index.html', objects_list=[{'title': title}])])


def registration_view(request, method, request_params):
    title = 'Регистрации'
    if method == 'POST':
        type_ = 'Person'
        id = None
        user_type = request_params["user_type"]
        lastname = request_params["lastname"]
        firstname = request_params["firstname"]
        email = request_params["email"]
        password = request_params["password"]
        site.create(type_, id, lastname, firstname, user_type, email, password)
    return Response(OK, [render('registration.html', objects_list=[{'title': title}])])


def users_list(request, method, request_params):
    return Response(OK, [render('users-list.html', objects_list=site.get('Person'))])


def students_list(request, method, request_params):
    return Response(OK, [render('students-list.html', objects_list=site.get('Person'))])


def teachers_list(request, method, request_params):
    return Response(OK, [render('teachers-list.html', objects_list=site.get('Person'))])


@debug
def create_category_view(request, method, request_params):
    if method == 'POST':
        # метод пост
        site.create('Category', request_params['name'])
        return Response(OK, [render('create-category.html')])
    else:
        categories = site.get('Category')
        return Response(OK, [render('create-category.html', categories=categories)])


@debug
def create_course_view(request, method, request_params):
    if method == 'POST':
        # метод пост
        name = request_params['name']
        form_course = request_params['form_course']
        type_course = request_params['type_course']
        category_name = request_params['category_name']
        if category_name:
            course = site.create('Course', category_name, name, form_course, type_course)
        else:
            # редирект
            return Response(REDIRECT, [render('create-category.html')])

        return Response(OK, [render('create-course.html')])
    else:
        categories = site.get('Category')
        return Response(OK, [render('create-course.html', categories=categories)])


@debug
def contact_view(request, method, request_params):
    if method == 'POST':
        print(request_params)  # работаем с введенными параметрами
    data = request.datas.get('data', None)
    title = 'Контакты'
    return Response(OK, [render('contact.html', object_list=[{'title': title}, {'data': data}])])


@debug
def course_list(request, method, request_params):
    return Response(OK, [render('course-list.html', objects_list=site.get('Course'))])


@debug
def copy_course(request, method, request_params):
    name = request_params['name']
    old_course = site.get('Course')
    if old_course:
        site.get_copy(name, old_course)
    return Response(OK, [render('course-list.html', objects_list=site.get('Course'))])


@debug
def category_list(request, method, request_params):
    category = site.get('Category')
    course = site.get('Course')
    return Response(OK, [render('category-list.html', objects_list=[{'category': category}, {'course': course}])])


@debug
def view_404(request):
    title = 'Not_Found'
    return Response(NOT_FOUND, [render('index.html', objects_list=[{'title': title}])])


urls = {
    '/': main_view,
    '/create-category/': create_category_view,
    '/create-course/': create_course_view,
    '/contact/': contact_view,
    '/category-list/': category_list,
    '/course-list/': course_list,
    '/copy-course/': copy_course,
    '/registration-form/': registration_view,
    '/students-list/': students_list,
    '/teachers-list/': teachers_list,
    '/users-list/': users_list,
}
