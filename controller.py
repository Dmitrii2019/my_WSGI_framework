from logging import log

from base.data_mapper import TrainingSite
from decorators.debug import debug
from setting import OK, NOT_FOUND, REDIRECT
from wavy.template import render
from wavy.utilities import Response, PrototypeMixin

site = TrainingSite()


@debug
def main_view(request, method, request_params):
    if method == 'POST':
        if 'category' in request_params:
            site.add_course_to_category(request_params['category'], request_params['course'])
        elif 'person' in request_params:
            site.add_person_to_course(request_params['person'], request_params['course'])

    categories = site.get('Category')
    course = site.get('Course')
    student = site.get('Person')
    return Response(OK, [render('index.html', objects_list=[
                            {'categories': categories},
                            {'course': course},
                            {'student': student}])])


def registration_view(request, method, request_params):
    title = 'Регистрации'
    if method == 'POST':
        user_type = request_params["user_type"]
        lastname = request_params["lastname"]
        firstname = request_params["firstname"]
        email = request_params["email"]
        password = request_params["password"]
        site.create('Person', None, lastname, firstname, user_type, 'no', email, password)
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
        site.create('Category', None, request_params['name'], 'нет')

    categories = site.get('Category')
    return Response(OK, [render('category.html', categories=categories)])


@debug
def create_course_view(request, method, request_params):
    if method == 'POST':
        name = request_params['name']
        form_course = request_params['form_course']
        type_course = request_params['type_course']
        if name:
            site.create('Course', None, name, form_course, type_course)

    course = site.get('Course')
    return Response(OK, [render('course.html', course=course)])


@debug
def contact_view(request, method, request_params):
    if method == 'POST':
        print(request_params)  # работаем с введенными параметрами
    data = request.datas.get('data', None)
    title = 'Контакты'
    return Response(OK, [render('contact.html', object_list=[{'title': title}, {'data': data}])])


@debug
def copy_course(request, method, request_params):
    id = request_params['id']
    try:
        old_course = site.find_by_id('Course', id)
    except Exception as e:
        return view_404(request)

    if old_course:
        new_name = f'copy_{old_course.name}'
        new_course = PrototypeMixin.clone(old_course)
        new_course.name = new_name
        site.create('Course', None, new_course.name, new_course.form_course, new_course.type_course)
    return Response(OK, [render('course.html', course=site.get('Course'))])


@debug
def view_404(request):
    title = 'Not_Found'
    return Response(NOT_FOUND, [render('404.html', objects_list=[{'title': title}])])


urls = {
    '/': main_view,
    '/category/': create_category_view,
    '/course/': create_course_view,
    '/contact/': contact_view,
    '/copy-course/': copy_course,
    '/registration-form/': registration_view,
    '/students-list/': students_list,
    '/teachers-list/': teachers_list,
    '/users-list/': users_list,
}
